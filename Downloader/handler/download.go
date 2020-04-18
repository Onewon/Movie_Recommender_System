package handler

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	cfg "rest_server/config"
	"rest_server/util"
	"time"
)

func fetch(url string) []byte {
	fmt.Println("Fetch Url", url)
	client := &http.Client{}
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("User-Agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Http get err:", err)
		return []byte("")
	}
	if resp.StatusCode != 200 {
		fmt.Println("Http status code:", resp.StatusCode)
		return []byte("")
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Read error", err)
		return []byte("")
	}
	return body
}

func parseUrl(filename string, url string, ch chan bool) {
	//data
	body := fetch(url)
	time.Sleep(1 * time.Second)

	//Write file

	//分区
	var filenamelength int = len([]rune(filename))
	// if filename[filenamelength-3:] == "jpg" {
	// 	div_name = strings.Replace(filename, ".jpg", "", 1)
	// } else if filename[filenamelength-3:] == "png" {
	// 	div_name = strings.Replace(filename, ".png", "", 1)
	// }
	var div_dir string
	div_dir = cfg.ProjectStaticDir + "/" + filename[filenamelength-2:]

	//判断存在，创建文件夹
	if !util.IsExist(div_dir) {
		os.MkdirAll(div_dir, 0744)
	}

	fpath := div_dir + "/" + filename + ".jpg"
	err := ioutil.WriteFile(fpath, body, 0744) //*.jpg
	if err != nil {
		fmt.Println("Write File error", err)
	}
	ch <- true
}

func downloader(ntimes int, urls map[string]interface{}) {
	start := time.Now()
	ch := make(chan bool)
	for key, url := range urls {
		go parseUrl(key, string(url.(string)), ch)
	}

	// for i := 1; i < ntimes+1; i++ {
	// 	go parseUrl(strconv.Itoa(i), ch)
	// }

	for i := 1; i < ntimes+1; i++ {
		<-ch
	}

	elapsed := time.Since(start)
	fmt.Println("Took %s", elapsed)
	fmt.Println("继续监听 127.0.0.1:7060...")
}
