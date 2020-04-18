/*
	Post 127.0.0.1/crawl

	{'total': N,
	'crawl_list':{file1: url1,
				  file2: url2,
				  file3: url3, },
	}

	Response: OK
*/
package main

import (
	"fmt"
	"net/http"
	cfg "rest_server/config"
	"rest_server/handler"
)

func main() {
	http.HandleFunc("/crawl", handler.CrawlHandler)
	fmt.Printf("REST服务启动中，开始监听 %s...\n", cfg.ServiceHost)

	err := http.ListenAndServe(cfg.ServiceHost, nil)
	if err != nil {
		fmt.Printf("Failed to start server, err:%s", err.Error())
	}
}
