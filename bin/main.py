import os

fix_format = {

}
class WorkDirManager:

    def __init__(self):
        self.work_dir = os.path.dirname(os.getcwd())    # 获取主程序工作目录
        self.origin_dir = self.touch_dir("origin")
        self.output_dir = self.touch_dir("output")
        self.cache_dir = self.touch_dir("caches")
        print("init work root dir:", self.work_dir)

    def touch_dir(self, fold_name):
        """
        获取/创建指定目录
        :param fold_name: 目标文件夹名称
        :return: 完整目录路径
        """
        target_dir = os.path.join(self.work_dir, fold_name)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)  # 自动创建多级目录
            print(f"已创建目录: {target_dir}")
        else:
            print(f"目录已存在: {target_dir}")

        return target_dir
    def get_origin_files(self):
        """
        获取origin目录下的所有文件，并返回（文件名列表），若列表内存在哈希值相同文件则重命名
        :return:
        """
        files = os.listdir(self.origin_dir)
        return files
    pass

alice = WorkDirManager()
