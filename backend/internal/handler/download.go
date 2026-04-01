package handler

import (
	"net/http"
	"os"
	"path/filepath"

	"et-backend/internal/service"
	"github.com/gin-gonic/gin"
)

// DownloadWindows 获取 Windows 下载链接
func DownloadWindows(c *gin.Context) {
	url := service.GetDownloadURL("windows", "x86_64", "")
	c.JSON(http.StatusOK, gin.H{
		"code": 0,
		"data": url,
	})
}

// DownloadAndroid 获取 Android 下载链接
func DownloadAndroid(c *gin.Context) {
	url := service.GetDownloadURL("android", "", "")
	c.JSON(http.StatusOK, gin.H{
		"code": 0,
		"data": url,
	})
}

// ServeDownload 提供文件下载服务
func ServeDownload(c *gin.Context) {
	filename := c.Param("filename")
	downloadDir := filepath.Join(os.Getenv("ET_CONFIG_DIR"), "..", "downloads")
	filePath := filepath.Join(downloadDir, filename)
	
	// 安全检查：确保文件在下载目录内
	if !service.IsPathSafe(filePath, downloadDir) {
		c.JSON(http.StatusForbidden, gin.H{"error": "Access denied"})
		return
	}
	
	c.File(filePath)
}
