package handler

import (
	"encoding/json"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

// ListNodes 获取节点列表
func ListNodes(c *gin.Context) {
	etBinDir := os.Getenv("ET_BIN_DIR")
	cliPath := filepath.Join(etBinDir, "easytier-cli")

	cmd := exec.Command(cliPath, "--output", "json", "peer")
	output, err := cmd.Output()
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"code": -1,
			"data": "Failed to get peers: " + err.Error(),
		})
		return
	}

	var peers interface{}
	if err := json.Unmarshal(output, &peers); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"code": -1,
			"data": "Failed to parse peers: " + err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"code": 0,
		"data": peers,
	})
}
