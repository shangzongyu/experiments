package main

import (
	"fmt"
	"log"
	"time"

	"github.com/nats-io/nats.go"
)

func main() {
	// 连接到 NATS 服务器
	url := "nats://127.0.0.1:4222,nats://127.0.0.1:4223,nats://127.0.0.1:4224"
	nc, err := nats.Connect(url)
	if err != nil {
		log.Fatalf("连接 NATS 服务器失败: %v", err)
	}
	defer nc.Close()

	// 定义发布和订阅的主题
	subject := "demo.subject"

	// 订阅主题
	_, err = nc.Subscribe(subject, func(msg *nats.Msg) {
		fmt.Printf("收到消息: %s\n", string(msg.Data))
	})
	if err != nil {
		log.Fatalf("订阅主题失败: %v", err)
	}
	fmt.Println("已订阅主题:", subject)

	// 向主题发布消息
	for i := 1; i <= 5; i++ {
		message := fmt.Sprintf("消息 %d", i)
		err := nc.Publish(subject, []byte(message))
		if err != nil {
			log.Printf("发布消息失败: %v", err)
			continue
		}
		fmt.Printf("已发布: %s\n", message)
		time.Sleep(1 * time.Second) // 每次发布后等待1秒
	}

	// 保持订阅者运行以接收消息
	select {} // 无限阻塞以保持程序运行
}
