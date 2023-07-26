package model

import (
	"gorm.io/gorm"
)

// Model Country
type Country struct {
	gorm.Model
	ID       int    `gorm:"autoIncrement"`
	Code3    string `gorm:"size:3;unique"`
	Currency string
	Name     string `gorm:"unique"`
	Year     int
	PPP      float64
}

// Model Config
type Config struct {
	gorm.Model
	ID    int    `gorm:"autoIncrement"`
	Key   string `gorm:"unique"`
	Value string
}
