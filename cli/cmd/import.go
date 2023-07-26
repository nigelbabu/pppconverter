package cmd

import (
	"encoding/csv"
	"io"
	"log"
	"os"
	"strconv"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"github.com/nigelbabu/pppconverter/model"
)

// importCmd represents the import command
var importCmd = &cobra.Command{
	Use:   "import",
	Short: "Import the PPP data from a file",
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
			var year int64
			year, err = strconv.ParseInt(row[2], 10, 32)
			if err != nil {
				log.Fatalf("failed to convert %d to float", row[2])
			}
			var ppp float64
			ppp, err = strconv.ParseFloat(row[3], 32)
			if err != nil {
				log.Fatalf("failed to convert %f to float", row[3])
			}
			record := &model.Country{
				Code3: row[1],
				Name:  row[0],
				Year:  int(year),
				PPP:   float64(ppp),
			}
			db.Create(record)
		}
	},
}

func init() {
	rootCmd.AddCommand(importCmd)
	importCmd.Flags().StringP("file", "f", "", "Path to the CSV file with PPP data")
	importCmd.Flags().StringP("database", "d", "temp.db", "Path to the CSV file with PPP data")
	viper.BindPFlag("database", importCmd.Flags().Lookup("database"))
	importCmd.MarkFlagRequired("file")
}
