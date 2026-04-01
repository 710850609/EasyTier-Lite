package handler

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

// GetLogs 获取日志（WebSocket 或 SSE 接口）
func GetLogs(c *gin.Context) {
	// 这里可以实现 WebSocket 或 SSE 来实时推送日志
	// 简化版本：返回静态日志内容
	logFile := filepath.Join(os.Getenv("ET_CONFIG_DIR"), "..", "server.log")
	
	content, err := os.ReadFile(logFile)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"code": 0,
			"data": "",
		})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"code": 0,
		"data": string(content),
	})
}
