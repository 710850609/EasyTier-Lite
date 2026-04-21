package assets

import (
	_ "embed"
)

//go:embed icon.png
var IconPNG []byte

//go:embed icon.ico
var IconICO []byte

//go:embed icon.icns
var IconICNS []byte

// GetIcon 获取当前平台的图标
func GetIcon(platform string) []byte {
	switch platform {
	case "windows":
		if len(IconICO) > 0 {
			return IconICO
		}
		return IconPNG
	case "darwin":
		if len(IconICNS) > 0 {
			return IconICNS
		}
		return IconPNG
	default:
		return IconPNG
	}
}
