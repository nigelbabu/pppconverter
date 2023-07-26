package main

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	"github.com/nigelbabu/pppconverter/helper"
	"github.com/nigelbabu/pppconverter/model"
)

var (
	db            *gorm.DB
	cached        cachedData
	cacheDuration = 1 * time.Hour
)

type cachedData struct {
	countries      []model.Country
	conversionRate string
	Time           time.Time
}

type result struct {
	SourceAmount   string
	TargetAmount   string
	SourceCountry  string
	SourceCurrency string
	TargetCountry  string
	TargetCurrency string
}

type formData struct {
	SourceCountry int   `form:"from_country"`
	Salary        int64 `form:"salary"`
	TargetCountry int   `form:"to_country"`
}

func FetchCountries() ([]model.Country, error) {
	if time.Now().Before(cached.Time) && len(cached.countries) != 0 {
		return cached.countries, nil
	}
	var countries []model.Country
	results := db.Find(&countries)
	if results.Error != nil {
		return nil, results.Error
	}
	cached.countries = countries
	cached.Time = time.Now().Add(cacheDuration)
	return countries, nil
}

func FetchConversionRate() (string, error) {
	if time.Now().Before(cached.Time) && cached.conversionRate != "" {
		return cached.conversionRate, nil
	}
	var cfg model.Config
	results := db.Where(model.Config{Key: "gbp_rate"}).First(&cfg)
	if results.Error != nil {
		return "", results.Error
	}
	cached.conversionRate = cfg.Value
	cached.Time = time.Now().Add(cacheDuration)
	return cfg.Value, nil
}

func homePage(c *gin.Context) {
	// Fetch country data for all requests
	countries, err := FetchCountries()
	if err != nil {
		log.Println("Failed to read DB: ", err)
	}
	conversionRate, err := FetchConversionRate()
	if err != nil {
		log.Println("Failed to read DB: ", err)
	}

	var srcCountry, targetCountry model.Country
	var form formData
	var r result
	if c.ShouldBind(&form) == nil && c.Request.Method == http.MethodPost {
		srcCountry.ID = form.SourceCountry
		targetCountry.ID = form.TargetCountry
		db.First(&srcCountry)
		db.First(&targetCountry)
		sourceAmt, err := helper.FormatMoney(float64(form.Salary))
		if err != nil {
			log.Printf("Failed to convert money: %s", err)
		}
		targetAmt, err := helper.FormatMoney((float64(form.Salary) / srcCountry.PPP) * targetCountry.PPP)
		if err != nil {
			log.Printf("Failed to convert money: %s", err)
		}
		r = result{
			SourceAmount:   sourceAmt,
			TargetAmount:   targetAmt,
			SourceCountry:  srcCountry.Name,
			SourceCurrency: srcCountry.Currency,
			TargetCountry:  targetCountry.Name,
			TargetCurrency: targetCountry.Currency,
		}
		log.Println("Salary", form.Salary)
	}

	c.HTML(http.StatusOK, "index.html", gin.H{
		//TODO: Fetch from DB and round up correctly
		"ConversionRate":  conversionRate,
		"Countries":       countries,
		"FormData":        form,
		"Result":          r,
		"GoogleAnalytics": viper.GetString("google_analytics"),
	})
}

func setupRouter() *gin.Engine {
	// Disable Console Color
	// gin.DisableConsoleColor()
	r := gin.Default()

	// Serve static files
	r.Static("/static", viper.GetString("static"))

	// Load all the template files
	r.LoadHTMLGlob(viper.GetString("templates"))

	// Ping test
	r.GET("/ping", func(c *gin.Context) {
		c.String(http.StatusOK, "pong")
	})

	// Home Page
	r.GET("/", homePage)
	r.POST("/", homePage)

	return r
}

func setupDatabase() (*gorm.DB, error) {
	db, err := gorm.Open(sqlite.Open(viper.GetString("database")), nil)
	if err != nil {
		return nil, err
	}
	return db, nil
}

func setupConfig() error {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	viper.SetDefault("database", "temp.db")
	viper.SetDefault("static", "./static")
	viper.SetDefault("templates", "./templates/*.html")
	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			// Ignore if config file not found
			return nil
		}
		return fmt.Errorf("Failed to load config: %s", err)
	}
	return nil
}

func main() {
	var err error
	if err = setupConfig(); err != nil {
		log.Fatal(err)
	}
	// Assigning to global DB variable
	db, err = setupDatabase()
	if err != nil {
		log.Fatal(err)
	}
	r := setupRouter()
	// Listen and Server in 0.0.0.0:8080
	r.Run(":8080")
}
