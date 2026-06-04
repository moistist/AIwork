#!/usr/bin/env python3
import os
import zipfile
from pathlib import Path

def create_skill_zip(skill_dir, output_dir):
    """为单个技能创建 ZIP 包"""
    skill_name = os.path.basename(skill_dir)
    zip_path = os.path.join(output_dir, f"{skill_name}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历技能目录
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # 计算在 ZIP 中的路径
                arcname = os.path.relpath(file_path, start=os.path.dirname(skill_dir))
                zipf.write(file_path, arcname)
    
    print(f"✓ 创建: {zip_path}")
    return zip_path

def main():
    # 技能源目录
    skills_source = "/workspace/gsap-skills/skills"
    # ZIP 输出目录
    output_dir = "/workspace/gsap_skills_zips"
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 所有技能
    skill_names = [
        "gsap-core",
        "gsap-timeline",
        "gsap-scrolltrigger",
        "gsap-plugins",
        "gsap-utils",
        "gsap-react",
        "gsap-performance",
        "gsap-frameworks"
    ]
    
    print("正在为每个技能创建 ZIP 包...")
    print("=" * 50)
    
    for skill_name in skill_names:
        skill_dir = os.path.join(skills_source, skill_name)
        if os.path.exists(skill_dir):
            create_skill_zip(skill_dir, output_dir)
        else:
            print(f"✗ 未找到: {skill_dir}")
    
    print("=" * 50)
    print(f"\n所有 ZIP 包已保存到: {output_dir}")
    
    # 列出创建的文件
    print("\n创建的文件列表:")
    for file in sorted(os.listdir(output_dir)):
        if file.endswith(".zip"):
            file_path = os.path.join(output_dir, file)
            size = os.path.getsize(file_path)
            print(f"  - {file} ({size:,} 字节)")

if __name__ == "__main__":
    main()
