from scraper import Scraper
# from embedder import Embedder
from lecture_parser import Parser
from lecture_manager import LectureManager
from db import Storage
import os
from queryer import Queryer

#manager = LectureManager()
#manager.update_lectures()

#storage = Storage()
#print(storage.get_lessons())

queryer = Queryer()
output2 = queryer.summarizer(["Docker can package an application and its dependencies in a virtual container that can run on any Linux, Windows, or macOS computer. This enables the application to run in a variety of locations, such as on-premises, in public (see decentralized computing, distributed computing, and cloud computing) or private cloud.[10] When running on Linux, Docker uses the resource isolation features of the Linux kernel (such as cgroups and kernel namespaces) and a union-capable file system (such as OverlayFS)[11] to allow containers to run within a single Linux instance, avoiding the overhead of starting and maintaining virtual machines.[12] Docker on macOS uses a Linux virtual machine to run the containers.","Because Docker containers are lightweight, a single server or virtual machine can run several containers simultaneously.[14] A 2018 analysis found that a typical Docker use case involves running eight containers per host, and that a quarter of analyzed organizations run 18 or more per host.[15] It can also be installed on a single board computer like the Raspberry Pi","The Linux kernel's support for namespaces mostly[17] isolates an application's view of the operating environment, including process trees, network, user IDs and mounted file systems, while the kernel's cgroups provide resource limiting for memory and CPU.[18] Since version 0.9, Docker includes its own component (called libcontainer) to use virtualization facilities provided directly by the Linux kernel, in addition to using abstracted virtualization interfaces via libvirt, LXC and systemd-nspawn.[19][9][10][20]"])
print(output2)

# storage = Storage()
# storage.db.delete_collection('Lessons')
# storage.db.delete_collection('Lectures')
# print(storage.db.list_collections())


# srt_dir = scraper.execute()
# scraper.get_embed_link("https://mediaspace.wisc.edu/media/Tyler%20Caraza-Harter-Agriculture%20125-09_04_24-14%3A18%3A34/1_sbftfkbl")

# download_dir = os.getenv('SRT_PATH')
# embedder = Embedder(download_dir)
# embedder.embed("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")

# p = Parser()
# c = p.parse_chunks("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")
# print(c)

# storage = Storage()
# storage.db.delete_collection("Lectures")
# print(storage.db.list_collections())
# storage.add_lecture("/Users/avitirto/Documents/ML/KalturaSearchSystem/lecture_srt/Tyler Caraza-Harter-Agriculture 125-09_04_24-14_18_34 (1).srt")

# r = storage.query("What is the main difference between a CPU and GPU?")
# print(r)
# print(len(r))