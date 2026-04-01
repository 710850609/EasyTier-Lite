package service

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

const (
	etMinVersion = "2.5.0"
	githubProxy  = "https://ghfast.top"
)

// GetDownloadURL 获取下载链接
func GetDownloadURL(system, arch, version string) string {
	if version == "" {
		version = getLatestVersion()
	}
	
	var packageName string
	if system == "android" {
		packageName = "app-universal-release.apk"
	} else {
		packageName = fmt.Sprintf("easytier-%s-%s-v%s.zip", system, arch, version)
	}
	
	downloadURL := fmt.Sprintf("https://github.com/EasyTier/EasyTier/releases/download/v%s/%s", version, packageName)
	return getProxyURL(downloadURL)
}

// GetPackageName 获取包名
func GetPackageName(system, arch, version string) string {
	if system == "android" {
		return "app-universal-release.apk"
	}
	if version == "" {
		version = getLatestVersion()
	}
	return fmt.Sprintf("easytier-%s-%s-v%s.zip", system, arch, version)
}

// DownloadPackage 下载包
func DownloadPackage(downloadDir, system, arch, version string) (string, error) {
	if version == "" {
		version = getLatestVersion()
	}
	
	packageName := GetPackageName(system, arch, version)
	downloadFile := filepath.Join(downloadDir, packageName)
	
	// 检查缓存
	if _, err := os.Stat(downloadFile); err == nil {
		return downloadFile, nil
	}
	
	// 下载
	downloadURL := fmt.Sprintf("https://github.com/EasyTier/EasyTier/releases/download/v%s/%s", version, packageName)
	return downloadFile, downloadFileFromURL(downloadURL, downloadFile)
}

func getLatestVersion() string {
	apiURL := "https://api.github.com/repos/EasyTier/EasyTier/releases/latest"
	
	resp, err := http.Get(apiURL)
	if err != nil {
		return etMinVersion
	}
	defer resp.Body.Close()
	
	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return etMinVersion
	}
	
	tagName, ok := result["tag_name"].(string)
	if !ok {
		return etMinVersion
	}
	
	// 去掉 v 前缀
	version := strings.TrimPrefix(tagName, "v")
	
	// 检查最小版本
	if compareVersions(version, etMinVersion) < 0 {
		return etMinVersion
	}
	
	return version
}

func getProxyURL(originalURL string) string {
	return githubProxy + "/" + originalURL
}

func downloadFileFromURL(url, filepath string) error {
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("bad status: %s", resp.Status)
	}
	
	// 创建临时文件
	tmpFile := filepath + ".tmp"
	out, err := os.Create(tmpFile)
	if err != nil {
		return err
	}
	defer out.Close()
	
	// 写入文件
	_, err = out.ReadFrom(resp.Body)
	if err != nil {
		os.Remove(tmpFile)
		return err
	}
	
	// 重命名
	return os.Rename(tmpFile, filepath)
}

// IsPathSafe 检查路径是否在允许的目录内
func IsPathSafe(path, allowedDir string) bool {
	absPath, err := filepath.Abs(path)
	if err != nil {
		return false
	}
	
	absAllowed, err := filepath.Abs(allowedDir)
	if err != nil {
		return false
	}
	
	return strings.HasPrefix(absPath, absAllowed)
}

// compareVersions 比较版本号
func compareVersions(v1, v2 string) int {
	parts1 := strings.Split(v1, ".")
	parts2 := strings.Split(v2, ".")
	
	for i := 0; i < len(parts1) && i < len(parts2); i++ {
		var n1, n2 int
		fmt.Sscanf(parts1[i], "%d", &n1)
		fmt.Sscanf(parts2[i], "%d", &n2)
		
		if n1 < n2 {
			return -1
		}
		if n1 > n2 {
			return 1
		}
	}
	
	return len(parts1) - len(parts2)
}
