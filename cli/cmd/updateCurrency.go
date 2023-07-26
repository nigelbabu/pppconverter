package cmd

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"github.com/nigelbabu/pppconverter/model"
)

type exchangeRate struct {
	Rates map[string]float64 `json:"rates"`
}

// updateCurrencyCmd represents the updateCurrency command
var openExchange = "http://openexchangerates.org/api/latest.json"
var updateCurrencyCmd = &cobra.Command{
	Use:   "updateCurrency",
	Short: "Update currency conversion rate for example",
	Run: func(cmd *cobra.Command, args []string) {
		resp, err := http.Get(fmt.Sprintf("%s?app_id=%s",
			openExchange,
			viper.GetString("open_exchange")))
		if err != nil {
			log.Fatalf("failed to call open exchange: %s", err)
		}
		defer resp.Body.Close()
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			log.Fatalf("failed to read response: %s", err)
		}
		var r exchangeRate
		if err := json.Unmarshal(body, &r); err != nil {
			log.Fatalf("failed to unmarshall JSON: %s", err)
		}
		dbPath, err := cmd.Flags().GetString("database")
		if err != nil {
			log.Fatal("Failed to get DB flag")
		}
		db, err := gorm.Open(sqlite.Open(dbPath), &gorm.Config{})
		if err != nil {
			log.Fatalf("Failed to open DB: %s", err)
		}
		var cfg model.Config
		db.Where(model.Config{Key: "gbp_rate"}).First(&cfg)
		fmt.Printf("Current value: %s, New value: %.2f\n", cfg.Value, r.Rates["GBP"]*100)
		cfg.Key = "gbp_rate"
		cfg.Value = fmt.Sprintf("%.2f", r.Rates["GBP"]*100)
		db.Save(&cfg)

	},
}

func init() {
	rootCmd.AddCommand(updateCurrencyCmd)
	updateCurrencyCmd.Flags().StringP("database", "d", "temp.db", "Path to the CSV file with PPP data")
	viper.BindPFlag("database", updateCurrencyCmd.Flags().Lookup("database"))
}
