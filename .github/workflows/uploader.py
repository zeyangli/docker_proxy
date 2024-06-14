import os
import sys
import subprocess
import json

def upload_docker_images(images, registry_url, username, password):
    for image in images:
        image_name = image['name']
        image_tag = image['tag']
        
        # 构建完整的镜像标签
        full_image_tag = f"{registry_url}/{image_name}:{image_tag}"
        
        # 登录到 Docker Registry
        login_command = f"docker login {registry_url} -u {username} -p {password}"
        subprocess.run(login_command, shell=True, check=True)
        
        # 打标签并推送镜像
        tag_command = f"docker tag {image_name}:{image_tag} {full_image_tag}"
        push_command = f"docker push {full_image_tag}"
        
        subprocess.run(tag_command, shell=True, check=True)
        subprocess.run(push_command, shell=True, check=True)
        
        # 登出 Docker Registry
        logout_command = f"docker logout {registry_url}"
        subprocess.run(logout_command, shell=True, check=True)

if __name__ == "__main__":
  username = sys.argv[1]
  password = sys.argv[2]
  registry_url = sys.argv[3]
  # 读取 JSON 文件
  with open('images.json') as file:
      images = json.load(file)
      for i in images:
          upload_docker_images(i["source"], i["target"],registry_url, username, password)
