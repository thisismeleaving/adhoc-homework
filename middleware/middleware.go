package main

import (
	"crypto/sha1"
	"encoding/hex"
	"flag"
	"fmt"
	"log"
	"net/http"
	"net/http/httptest"
	"sort"
	"strconv"
	"strings"
)

const (
	crlf       = "\r\n"
	colonspace = ": "
)

func ChecksumMiddleware(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		handler := func(w http.ResponseWriter, r *http.Request) {
			h.ServeHTTP(w, r)
		}

		rw := httptest.NewRecorder()
		handler(rw, r)

		hasher := sha1.New()
		header := rw.Header()
		checksum_headers_str := ""
		var keys []string

		for k := range header {
			keys = append(keys, k)
		}

		sort.Strings(keys)

		s := strconv.Itoa(rw.Code) + crlf

		for _, k := range keys {
			s += k + colonspace + header.Get(k) + crlf
		}

		checksum_headers_str += strings.Join(keys, ";")

		s += "X-Checksum-Headers: " + checksum_headers_str
		s += crlf + crlf + rw.Body.String()

		fmt.Println(s)

		hasher.Write([]byte(s))
		sha1_hash := hex.EncodeToString(hasher.Sum(nil))

		w.Header().Add("X-Checksum", sha1_hash)
		w.Header().Add("X-Checksum-Headers", checksum_headers_str)

		h.ServeHTTP(w, r)

	})
}

// Do not change this function.
func main() {
	var listenAddr = flag.String("http", ":8080", "address to listen on for HTTP")
	flag.Parse()

	http.Handle("/", ChecksumMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Foo", "bar")
		w.Header().Set("Content-Type", "text/plain")
		w.Header().Set("Date", "Sun, 08 May 2016 14:04:53 GMT")
		msg := "Curiosity is insubordination in its purest form.\n"
		w.Header().Set("Content-Length", strconv.Itoa(len(msg)))
		fmt.Fprintf(w, msg)
	})))

	log.Fatal(http.ListenAndServe(*listenAddr, nil))
}
