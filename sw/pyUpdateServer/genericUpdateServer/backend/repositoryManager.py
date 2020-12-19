import os
from pathlib import Path

from executorRepository.tools.os_tools import create_if_needed


class repositoryManager:

       def __init__(self,path):
              self.path = str(path)
              create_if_needed(self.path)

       def parse_repository(self):
              self.repos = {}
              components = os.listdir(self.path)
              for component in components:
                     self.repos[component] = {}
                     versions = os.listdir(Path(self.path + '/' + component))

                     for version in versions:
                            self.repos[component][version] = {}
                            versionfolder = str(Path(self.path + '/' + component + '/' + version))
                            zipfiles = os.listdir(versionfolder)
                            if (len(zipfiles)!=1):
                                   print('Erroneous repository structure at: ' + versionfolder)
                            else:
                                   self.repos[component][version]['zip'] = Path(versionfolder + '/' + zipfiles[0])
              return self.repos

       def get_component_path(self, component, version):
              self.parse_repository()
              if component in self.repos:
                     if version == 'latest':
                            version = self.latest_version(component)
                     if version in self.repos[component]:
                            return self.repos[component][version]['zip']
              return None

       def get_latest(self):
              latest = []
              self.parse_repository()
              for component in self.repos:
                     latest.append({
                            'component':  component,
                            'version': self.latest_version(component)
                     })

              return latest

       def latest_version(self, component):
              version = '0.0'
              for element in self.repos[component]:
                     [el_major, el_minor] = self.parse_version(element)
                     [latest_major, latest_minor] = self.parse_version(version)
                     if el_major >= latest_major:
                            latest_major = el_major
                            if el_minor >= latest_minor:
                                   latest_minor = el_minor
                     version = str(latest_major) + '.' + str(latest_minor)
              return version

       def set_new_component(self, file):
              if (file.filename.endswith('.zip')):
                     splitname = file.filename[:-4].split('_')
                     if len(splitname) == 2:
                            component = splitname[0]
                            version = splitname[1]
                            dirPath = Path(self.path + '/' + component)
                            create_if_needed(dirPath)
                            dirPath = Path(str(dirPath) + '/' + version)
                            create_if_needed(dirPath)
                            file.save(Path(str(dirPath) + '/'+  file.filename))
                            msg = 'New component added: ' + component + ' v' + version
                            print(msg)
                            return msg
                     else:
                            msg =  'Invalid file naming (component_version.zip)'
                            return msg
              else:
                     msg =  'Invalid file type (zip)'
                     return msg

       def parse_version(self, version_txt):
              point_pos = version_txt.find('.')
              major = int(version_txt[:point_pos])
              minor = int(version_txt[point_pos+1:])
              return [major, minor]
