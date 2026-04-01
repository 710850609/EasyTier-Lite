package util

import (
	"bytes"
	"os/exec"
	"time"
)

// RunCommand 执行命令并返回输出
func RunCommand(name string, args ...string) (string, error) {
	cmd := exec.Command(name, args...)
	
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	
	// 设置超时
	done := make(chan error)
	go func() {
		done <- cmd.Run()
	}()
	
	select {
	case err := <-done:
		if err != nil {
			return "", err
		}
		return stdout.String(), nil
	case <-time.After(time.Hour):
		cmd.Process.Kill()
		return "", exec.ErrWaitDelay
	}
}

// RunCommandWithTimeout 执行命令（带超时）
func RunCommandWithTimeout(timeout time.Duration, name string, args ...string) (string, error) {
	cmd := exec.Command(name, args...)
	
	var stdout bytes.Buffer
	cmd.Stdout = &stdout
	
	done := make(chan error)
	go func() {
		done <- cmd.Run()
	}()
	
	select {
	case err := <-done:
		if err != nil {
			return "", err
		}
		return stdout.String(), nil
	case <-time.After(timeout):
		cmd.Process.Kill()
		return "", exec.ErrWaitDelay
	}
}
