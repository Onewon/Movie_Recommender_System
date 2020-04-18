package handler

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	_ "strconv"
	"strings"
)

func CrawlHandler(w http.ResponseWriter, r *http.Request) {
	var data []byte = []byte("")
	if r.Method == "GET" {
		// 返回上传html页面
		// data, err := ioutil.ReadFile("./static/view/index.html")
		// if err != nil {
		// 	io.WriteString(w, "internel server error")
		// 	return
		// }
		io.WriteString(w, "Connect successful.")
		return
	} else if r.Method == "POST" {
		// 接收json
		var err error
		data, err = ioutil.ReadAll(r.Body)
		if err != nil {
			fmt.Println(err.Error())
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusOK)
	}
	var mapResult map[string]interface{}
	if data != nil {
		err := json.NewDecoder(strings.NewReader(string(data))).Decode(&mapResult)
		if err != nil {
			fmt.Println("json.NewDecoder 解码失败")
		}
	}
	n := mapResult["total"].(float64)
	ntimes := int(n)
	url_list := mapResult["crawl_url_list"].(map[string]interface{})
	// var url_listResult map[string]string
	// err = json.NewDecoder(strings.NewReader(url_list)).Decode(&url_listResult)
	// if err != nil {
	// 	fmt.Println("json.NewDecoder2 解码失败")
	// }
	for key, val := range url_list {
		fmt.Println(key + ":" + string(val.(string)))
	}
	downloader(ntimes, url_list)
	// if err != nil {
	// 	fmt.Println(err.Error())
	// 	w.WriteHeader(http.StatusInternalServerError)
	// 	return
	// }
	// file, head, err := r.FormFile("file")
	// if err != nil {
	// 	fmt.Printf("Failed to get data, err:%s\n", err.Error())
	// 	return
	// }
	// defer file.Close()

	// fileMeta := meta.FileMeta{
	// 	FileName: head.Filename,
	// 	Location: "/tmp/" + head.Filename,
	// 	UploadAt: time.Now().Format("2006-01-02 15:04:05"),
	// }

	// newFile, err := os.Create(fileMeta.Location)
	// if err != nil {
	// 	fmt.Printf("Failed to create file, err:%s\n", err.Error())
	// 	return
	// }
	// defer newFile.Close()
}
func CrawlSucHandler(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Crawl finished!")
}
