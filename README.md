### 配置步骤
  * 安置ticket文件到 dir
  * .zshrc文件中配置 alias ticket='python ~/dir/ticket/'
  * source .zshrc
  * 命令行运行 ticket -d 北京 合肥 20160623 可以查看信息
  * 查看命令日期格式:20160607,当时间为1位数需要补0

### 需求环境
  * python
  * 库: requests + docopt + colorama + stations + prettytable
