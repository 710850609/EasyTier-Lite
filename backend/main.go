package main

import (
	"log"
	"os"
	"path/filepath"

	"et-backend/internal/handler"
	"github.com/gin-gonic/gin"
)

func main() {
	// 设置环境变量
	setupEnv()

	// 创建 Gin 路由
	r := gin.Default()

	// 配置路由
	setupRoutes(r)

	// 启动服务器
	port := os.Getenv("PORT")
	if port == "" {
		port = "5666"
	}
	log.Printf("Server starting on port %s", port)
	if err := r.Run(":" + port); err != nil {
		log.Fatal(err)
	}
}

func setupEnv() {
	// 获取项目根目录
	execPath, err := os.Executable()
	if err != nil {
		log.Fatal(err)
	}
	execDir := filepath.Dir(execPath)
	
	// 设置默认环境变量
	if os.Getenv("ET_CONFIG_DIR") == "" {
		os.Setenv("ET_CONFIG_DIR", filepath.Join(execDir, "..", "temp", "config"))
	}
	if os.Getenv("ET_BIN_DIR") == "" {
		os.Setenv("ET_BIN_DIR", filepath.Join(execDir, "..", "app", "bin"))
	}
	
	// 确保配置目录存在
	os.MkdirAll(os.Getenv("ET_CONFIG_DIR"), 0755)
}

func setupRoutes(r *gin.Engine) {
	// API 路由组
	api := r.Group("/cgi/ThirdParty/EasyTier-Lite/api.cgi")
	{
		// 配置相关
		api.GET("/configs/needSetting", handler.NeedSetting)
		api.GET("/configs", handler.GetConfig)
		api.POST("/configs", handler.SaveConfig)
		api.GET("/configs/publicPeers", handler.PublicPeers)
		api.GET("/configs/download", handler.DownloadConfig)
		
		// 节点相关
		api.GET("/nodes", handler.ListNodes)
		
		// 日志相关
		api.GET("/logs", handler.GetLogs)
		
		// 下载相关
		api.GET("/download/windows", handler.DownloadWindows)
		api.GET("/download/android", handler.DownloadAndroid)
	}
	
	// 静态文件服务
	r.Static("/cgi/ThirdParty/EasyTier-Lite/index.cgi", "./dist")
}
