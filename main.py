'''
Description: 
Author: MOBval
Github: https://github.com/AshMOB
Date: 2023-11-21 09:44:46
LastEditors: Elysi4
LastEditTime: 2023-11-21 14:05:26
'''
# 功能：将当前目录下的jar包反编译并放入指定目录中，使用git提交，之后提交另一个版本的反编译进行比较

# 环境需求：python3，git，procyon

import argparse
import subprocess
import os
import zipfile
def init_git():
    git_path="./out"
    command=f"git init {git_path}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.stdout.read().decode("utf-8"))

def read_jar_list():
    # 获取当前文件夹的路径
    current_folder = os.getcwd()+"/f1rst"

    # 创建一个空列表来存储.jar文件的名称
    jar_files = []

    # 遍历当前文件夹中的所有文件
    for filename in os.listdir(current_folder):
        # 检查文件是否以.jar结尾
        if filename.endswith(".jar") and "procyon-decompiler" not in filename:
            # 如果是，则将其添加到列表中
            jar_files.append("f1rst/"+filename)
    # 打印列表
    return jar_files
    
def compile_jar(jar_name, jar_path):
    i=1
    for name in jar_name:
        subname=name.replace(".jar","")
        subname=subname.replace(f"{jar_path}/","")
        command=f"java -jar .\procyon-decompiler-0.6.0.jar -jar {name} -o out/{subname}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        for line in process.stdout:
            print(line.decode().strip())
            print(str(i)+"/"+str(len(jar_name)))
        process.wait()
        i+=1
        with zipfile.ZipFile(f"{name}", 'r') as zip_file:
            zip_file.extractall(f"out/{subname}")
        for root, dirs, files in os.walk(f"out/{subname}"):
            for file in files:
                if file.endswith(".class"):
                    os.remove(os.path.join(root, file))
    
def git_commit(jar_path):
    command="git -C ./out add ."
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.stdout.read().decode("utf-8"))
    command=f'git -C ./out commit --allow-empty -m "{jar_path} version"'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.stdout.read().decode("utf-8"))

def mkdir():
    # 在当前目录下创建名为'f1rst'的文件夹
    os.makedirs('f1rst', exist_ok=True)

    # 在当前目录下创建名为's2cond'的文件夹
    os.makedirs('s2cond', exist_ok=True)
    
def init():
    mkdir()
    
def run():
    init_git()
    compile_jar(read_jar_list(),"f1rst")
    git_commit("f1rst")
    compile_jar(read_jar_list(),"s2cond")
    git_commit("s2cond")
    
def banner():
    print("""
 ____  _  __  __     _            
|  _ \(_)/ _|/ _|   | | __ _ _ __ 
| | | | | |_| |_ _  | |/ _` | '__|
| |_| | |  _|  _| |_| | (_| | |   
|____/|_|_| |_|  \___/ \__,_|_|   
                                  """)
if __name__ == '__main__':
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", action="store_true", help="init")
    parser.add_argument("-r", "--run", action="store_true", help="run")
    args = parser.parse_args()
    if args.init:
        init()
    if args.run:
        run()