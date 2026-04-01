package handler

import (
	"net/http"
	"os"
	"path/filepath"

	"et-backend/internal/service"
	"github.com/gin-gonic/gin"
)

// NeedSetting 检查是否需要配置
func NeedSetting(c *gin.Context) {
	configDir := os.Getenv("ET_CONFIG_DIR")
	initFile := filepath.Join(configDir, ".init")
	
	_, err := os.Stat(initFile)
	needConfig := !os.IsNotExist(err)
	
	c.JSON(http.StatusOK, gin.H{
		"code": 0,
		"data": gin.H{"needConfig": needConfig},
	})
}

// GetConfig 获取配置
func GetConfig(c *gin.Context) {
	config, err := service.GetConfig()
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"code": -1,
			"data": err.Error(),
		})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"code": 0,
		"data": config,
	})
}

// SaveConfig 保存配置
func SaveConfig(c *gin.Context) {
	var data map[string]interface{}
	if err := c.ShouldBindJSON(&data); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"code": -1,
			"data": "Invalid JSON",
		})
		return
	}
	
	if err := service.SaveConfig(data); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"code": -1,
			"data": err.Error(),
		})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"code": 0,
		"data": "配置保存成功",
	})
}

// PublicPeers 获取公共节点列表
func PublicPeers(c *gin.Context) {
	peers := []map[string]string{
		{"label": "动态社区节点1", "uri": "https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-1.txt"},
		{"label": "动态社区节点2", "uri": "https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-2.txt"},
		{"label": "动态社区节点3", "uri": "https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-3.txt"},
		{"label": "动态社区节点4", "uri": "https://raw.githubusercontent.com/710850609/fpk-EasyTier-Lite/refs/heads/main/peers/peer-4.txt"},
	}
	
	c.JSON(http.StatusOK, gin.H{
		"code": 0,
		"data": peers,
	})
}

// DownloadConfig 下载配置文件
func DownloadConfig(c *gin.Context) {
	tmpFile, err := service.CopyConfig()
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"code": -1,
			"data": err.Error(),
		})
		return
	}
	
	c.FileAttachment(tmpFile, "et-fnos.toml")
}
