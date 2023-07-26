package cmd

import (
	"log"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"github.com/nigelbabu/pppconverter/model"
)

// dbInitCmd represents the dbInit command
var dbInitCmd = &cobra.Command{
	Use:   "dbInit",
	Short: "Initialize the SQL Database",
	Run: func(cmd *cobra.Command, args []string) {
		dbPath, err := cmd.Flags().GetString("database")
		if err != nil {
			log.Fatal("Failed to get DB flag")
		}
		db, err := gorm.Open(sqlite.Open(dbPath), &gorm.Config{})
		if err != nil {
			log.Fatalf("Failed to open DB: %s", err)
		}
		db.AutoMigrate(&model.Country{})
		db.AutoMigrate(&model.Config{})
	},
}

func init() {
	rootCmd.AddCommand(dbInitCmd)
	dbInitCmd.Flags().StringP("database", "d", "temp.db", "Path to the CSV file with PPP data")
	viper.BindPFlag("database", dbInitCmd.Flags().Lookup("database"))
}
