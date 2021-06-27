# site_packages_path is the packages folder, which in my case is:
site_packages_path = r"C:\Users\Ich\Desktop\Rocky_Hockey_Python\venv\lib\site-packages"

# path that you wanna add, which again in my case is
path_to_add = r"C:\Users\Ich\Desktop\Rocky_Hockey_Python"

f = open(site_packages_path + "\custom_path.pth", "a")
f.write(path_to_add)
