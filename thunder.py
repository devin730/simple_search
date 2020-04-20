from win32com.client import Dispatch
 
def down(url, name, format_):
    thunder = Dispatch('ThunderAgent.Agent64.1')
    # ThunderAgent.Agent.1 低版本可以试试这个
    # AddTask("下载地址", "另存为文件名", "保存目录", "任务注释", "引用地址", "开始模式", "只从原始地址下载", "从原始地址下载线程数")
    # thunder.AddTask('ftp://ygdy8:ygdy8@yg45.dydytt.net:8129/阳光电影www.ygdy8.com.蝙蝠侠：哥谭骑士.BD.720p.中英双字幕.mkv', 'movie.mkv')
    file_name = str(name)+str(format_)
    thunder.AddTask(url, file_name)
    thunder.CommitTasks()

if __name__ == '__main__':
    download_link = "ftp://ygdy8:ygdy8@yg39.dydytt.net:8013/阳光电影www.ygdy8.com.江湖儿女.BD.1080p.国语中字.mkv"
    name = "江湖儿女.BD"
    format_ = ".mkv"
    down(download_link, name, format_)