package cmd

import (
	"encoding/csv"
	"io"
	"log"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"github.com/nigelbabu/pppconverter/model"
)

// importCountriesCmd represents the importCountries command
var importCountriesCmd = &cobra.Command{
	Use:   "importCountries",
	Short: "Import the country data from a file",
	Run: func(cmd *cobra.Command, args []string) {
		dbPath, err := cmd.Flags().GetString("database")
		if err != nil {
			log.Fatal("Failed to get DB flag")
		}
		csvpath, err := cmd.Flags().GetString("file")
		if err != nil {
			log.Fatal("Could not find file flag")
		}

		db, err := gorm.Open(sqlite.Open(dbPath), &gorm.Config{})
		if err != nil {
			log.Fatalf("Failed to open DB: %s", err)
		}

		f, err := os.Open(csvpath)
		if err != nil {
			log.Fatalf("Failed to read file at %s", csvpath)
		}
		defer f.Close()
		csvreader := csv.NewReader(f)
		for {
			row, err := csvreader.Read()
			if err == io.EOF {
				break
			}
			if err != nil {
				log.Fatalf("Failed to read CSV: %s", err)
			}
			var country model.Country
			log.Println("Country: ", country)
			db.Where(model.Country{Code3: row[3]}).First(&country)
			if country.ID != 0 {
				country.Currency = row[14]
				log.Println("Country: ", country)
				db.Save(&country)
			}
		}
	},
}

func init() {
	rootCmd.AddCommand(importCountriesCmd)
	importCountriesCmd.Flags().StringP("file", "f", "", "Path to the CSV file with PPP data")
	importCountriesCmd.Flags().StringP("database", "d", "temp.db", "Path to the CSV file with country data")
	viper.BindPFlag("database", importCountriesCmd.Flags().Lookup("database"))
	importCountriesCmd.MarkFlagRequired("file")
}
