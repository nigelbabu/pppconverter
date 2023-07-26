package helper

import (
  "strings"
  "fmt"
  )


func FormatMoney(input float64) (string, error) {
  text := fmt.Sprintf("%.2f", input)
  var output strings.Builder
  var number bool
  var digits int
  for i := len(text) - 1; i >= 0; i-- {
    if text[i] == byte('.') {
      number = true
    }
    if digits == 4 {
      digits = 1
      if _, err := output.WriteString(","); err != nil {
        return "", err
      }
    }
    if err := output.WriteByte(text[i]); err != nil {
      return "", err
    }
    if number {
      digits++
    }
  }
  r := []rune(output.String())
  for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
    r[i], r[j] = r[j], r[i]
  }
  return string(r), nil
}
