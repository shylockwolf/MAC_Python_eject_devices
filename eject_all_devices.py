#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
弹出所有外置设备脚本

此脚本会安全地弹出Mac上所有挂载的外置设备，
包括USB驱动器、外部硬盘、SD卡等。
它会自动排除系统卷和主硬盘，避免意外卸载系统。
"""

import subprocess
import re
import sys
import time

def get_mounted_volumes():
    """
    获取所有挂载的卷信息
    返回格式: 字典 {卷名: 挂载点}
    """
    try:
        # 获取挂载点信息
        mount_result = subprocess.run(
            ["mount"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # 解析挂载点信息
        volumes = {}
        mount_lines = mount_result.stdout.strip().split('\n')
        
        for line in mount_lines:
            # 改进正则表达式，更好地处理包含特殊字符的卷名
            if ' on /Volumes/' in line:
                parts = line.split(' on ')
                if len(parts) >= 2:
                    mount_info = parts[1]
                    # 提取挂载点，去掉后面的文件系统信息
                    if ' (' in mount_info:
                        mount_point = mount_info.split(' (')[0]
                    else:
                        mount_point = mount_info
                    
                    if mount_point.startswith('/Volumes/'):
                        volume_name = mount_point.replace('/Volumes/', '')
                        volumes[volume_name] = mount_point
        
        return volumes
        
    except Exception:
        return {}

def is_system_volume(volume_name, mount_point):
    """
    判断是否为系统卷或主硬盘
    """
    # 系统卷标记
    system_volumes = [
        '/',  # 根目录
        '/System',
        '/Library',
        '/Users',
        '/Applications',
        '/Volumes/Macintosh HD',  # 默认系统卷名
        '/Volumes/Macintosh HD - Data'  # 默认数据卷名
    ]
    
    # 检查是否为系统卷
    if mount_point in system_volumes:
        return True
    
    # 检查卷名是否包含系统相关关键词
    system_keywords = ['macintosh', 'hd', 'system', 'boot']
    if any(keyword in volume_name.lower() for keyword in system_keywords):
        # 但允许用户有重名的外部卷，通过检查挂载点进一步确认
        if mount_point.startswith('/Volumes/') and mount_point not in system_volumes:
            return False
        return True
    
    return False

def eject_volume(volume_name, mount_point):
    """
    弹出指定的卷
    """
    try:
        # 使用diskutil eject命令安全弹出
        subprocess.run(
            ["diskutil", "eject", mount_point],
            check=True,
            capture_output=True
        )
        return True
    except Exception:
        # 如果直接弹出失败，尝试先卸载
        try:
            subprocess.run(
                ["diskutil", "unmount", mount_point],
                check=True,
                capture_output=True
            )
            return True
        except Exception:
            # 忽略卸载失败的错误，继续尝试其他设备
            return False

def main():
    """
    主函数
    """
    # 获取所有挂载的卷
    volumes = get_mounted_volumes()
    
    # 筛选出非系统的外置卷
    external_volumes = {}
    for volume_name, mount_point in volumes.items():
        if not is_system_volume(volume_name, mount_point) and mount_point.startswith('/Volumes/'):
            external_volumes[volume_name] = mount_point
    
    # 直接开始弹出设备，不显示警告和确认提示
    for volume_name, mount_point in external_volumes.items():
        eject_volume(volume_name, mount_point)
        # 短暂延迟，避免操作过快
        time.sleep(0.5)

if __name__ == "__main__":
    main()