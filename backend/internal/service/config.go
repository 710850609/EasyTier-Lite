package service

import (
	"bytes"
	"os"
	"path/filepath"

	"github.com/BurntSushi/toml"
)

// GetConfig 读取配置文件
func GetConfig() (map[string]interface{}, error) {
	configFile := getConfigFile()
	
	data, err := os.ReadFile(configFile)
	if err != nil {
		return nil, err
	}
	
	var config map[string]interface{}
	if err := toml.Unmarshal(data, &config); err != nil {
		return nil, err
	}
	
	// 转换 peer 和 proxy_network 格式
	if peers, ok := config["peer"].([]interface{}); ok {
		var peerURIs []string
		for _, p := range peers {
			if peerMap, ok := p.(map[string]interface{}); ok {
				if uri, ok := peerMap["uri"].(string); ok {
					peerURIs = append(peerURIs, uri)
				}
			}
		}
		config["peer"] = peerURIs
	}
	
	if proxies, ok := config["proxy_network"].([]interface{}); ok {
		var proxyCIDRs []string
		for _, p := range proxies {
			if proxyMap, ok := p.(map[string]interface{}); ok {
				if cidr, ok := proxyMap["cidr"].(string); ok {
					proxyCIDRs = append(proxyCIDRs, cidr)
				}
			}
		}
		config["proxy_network"] = proxyCIDRs
	}
	
	return config, nil
}

// SaveConfig 保存配置
func SaveConfig(data map[string]interface{}) error {
	configFile := getConfigFile()
	
	// 读取现有配置
	var existing map[string]interface{}
	if content, err := os.ReadFile(configFile); err == nil {
		toml.Unmarshal(content, &existing)
	}
	
	if existing == nil {
		existing = make(map[string]interface{})
	}
	
	// 深度合并
	deepMerge(existing, data)
	
	// 写入文件
	var buf bytes.Buffer
	if err := toml.NewEncoder(&buf).Encode(existing); err != nil {
		return err
	}
	
	if err := os.WriteFile(configFile, buf.Bytes(), 0644); err != nil {
		return err
	}
	
	// 删除 init 文件
	initFile := filepath.Join(os.Getenv("ET_CONFIG_DIR"), ".init")
	os.Remove(initFile)
	
	return nil
}

// CopyConfig 复制配置用于下载
func CopyConfig() (string, error) {
	config, err := GetConfig()
	if err != nil {
		return "", err
	}
	
	// 清空 IP，启用 DHCP
	config["ipv4"] = ""
	config["dhcp"] = true
	
	// 转换格式
	if peers, ok := config["peer"].([]string); ok {
		var peerObjs []map[string]string
		for _, p := range peers {
			peerObjs = append(peerObjs, map[string]string{"uri": p})
		}
		config["peer"] = peerObjs
	}
	
	if proxies, ok := config["proxy_network"].([]string); ok {
		var proxyObjs []map[string]string
		for _, p := range proxies {
			proxyObjs = append(proxyObjs, map[string]string{"cidr": p})
		}
		config["proxy_network"] = proxyObjs
	}
	
	// 写入临时文件
	tmpFile := "/tmp/EasyTier-Lite/config-copy.toml"
	os.MkdirAll(filepath.Dir(tmpFile), 0755)
	
	var buf bytes.Buffer
	if err := toml.NewEncoder(&buf).Encode(config); err != nil {
		return "", err
	}
	
	if err := os.WriteFile(tmpFile, buf.Bytes(), 0644); err != nil {
		return "", err
	}
	
	return tmpFile, nil
}

func getConfigFile() string {
	return filepath.Join(os.Getenv("ET_CONFIG_DIR"), "config.toml")
}

func deepMerge(base, override map[string]interface{}) {
	for key, value := range override {
		if value == nil {
			continue
		}
		
		if baseVal, ok := base[key].(map[string]interface{}); ok {
			if overrideVal, ok := value.(map[string]interface{}); ok {
				deepMerge(baseVal, overrideVal)
				continue
			}
		}
		base[key] = value
	}
}
