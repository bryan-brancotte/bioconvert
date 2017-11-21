package main

import ("fmt"
        "bufio"
        "log"
        "os"
        "strings"
)



func main() {

   filename := os.Args[1]

   var i = 0
   txt := ""
   fin, err := os.Open(filename)
   if err != nil {
       log.Fatal(err)
   }
   defer fin.Close()

   scanner := bufio.NewScanner(fin)
   for scanner.Scan() {
        txt = scanner.Text()
        if len(strings.TrimSpace(txt)) > 0 {
            if i%4 == 0 {
               fmt.Println(">" + txt[1:])
            } else if i%4 == 1 {
                fmt.Println(txt)
           }
           i = i + 1
        }
   }

   defer fin.Close()

}
