package helper

import (
  "testing"
  "fmt"
  )

func TestFormatMoney(t *testing.T) {
  var tests = []struct{
    input float64
    want string
  }{
    {
      input: 123.456,
      want: "123.46",
    },
    {
      input: 1001.123,
      want: "1,001.12",
    },
    {
      input: 19001.123,
      want: "19,001.12",
    },
    {
      input: 189001.123,
      want: "189,001.12",
    },
    {
      input: 1999001.123,
      want: "1,999,001.12",
    },
  }
  for _, tc := range tests {
    tc := tc
    t.Run(fmt.Sprintf("Input %f", tc.input), func(t *testing.T) {
      if got, err := FormatMoney(tc.input); got != tc.want {
        t.Errorf("Got %s, want %s: %v", got, tc.want, err)
      }
    })
  }

}
