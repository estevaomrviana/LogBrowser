from django.contrib.auth.models import User
from django.db import models
import paramiko
import stat


class SSHConnection(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ssh_connections'
    )
    hostname = models.CharField(max_length=255)
    port = models.IntegerField(default=22)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    remote_directory = models.CharField(max_length=255, default='/')

    def __str__(self):
        return f"{self.username}@{self.hostname}:{self.port}"
    
    def get_file_list(self, subfolder=""):
        file_list = []
        
        try:
            transport = paramiko.Transport((self.hostname, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            remote_path = f"{self.remote_directory}/{subfolder}".rstrip('/')
            
            for item in sftp.listdir_attr(remote_path):
                item_name = item.filename
                item_path = f"{remote_path}/{item_name}"
                item_type = 'directory' if stat.S_ISDIR(item.st_mode) else 'file'
                
                file_list.append({
                    'name': item_name,
                    'type': item_type,
                    'path': f"{subfolder}/{item_name}".strip('/')
                })

            sftp.close()
            transport.close()

            file_list.sort(key=lambda x: (x['type'] != 'directory', x['name'].lower()))

        except Exception as e:
            print(f"Erro ao conectar ao servidor SFTP: {e}")

        return file_list
    
    def read_file(self, file_path):
        try:
            transport = paramiko.Transport((self.hostname, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            full_path = f"{self.remote_directory}/{file_path}".rstrip('/')
            
            # Abrir e ler o conteúdo do arquivo
            with sftp.file(full_path, 'r') as file:
                file_content = file.read().decode('utf-8')  # Decodifica para string
            
            # Fecha a conexão
            sftp.close()
            transport.close()

            return file_content
        except Exception as e:
            print(f"Erro ao ler o arquivo {file_path}: {e}")
            return None


