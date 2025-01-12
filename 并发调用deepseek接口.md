
### **注册表参数表格**

| **注册表名称**          | **类型**      | **设置值(十进制)** |
|-------------------------|---------------|--------------|
| MaxUserPort            | REG_DWORD     | 65534        |
| TcpTimedWaitDelay      | REG_DWORD     | 30           |
| MaxFreeConnections | REG_DWORD | 3000         |
| MaxFreeTcbs | REG_DWORD | 100000       |
| TcpNumConnections | REG_DWORD | 65535        |


---

### **修改注册表的步骤**

1. **打开注册表编辑器**：
   - 按下 `Win + R`，输入 `regedit`，按回车键。
   - 在弹出的用户账户控制窗口中选择“是”。

2. **备份注册表**：
   - 在注册表编辑器中，点击左上角的“文件” > “导出”。
   - 选择一个保存位置并命名备份文件，确保选中“全部”范围，点击“保存”。

3. **找到对应路径并修改键值**：
   - 根据需要修改的参数，定位到以下路径：
     ```
     HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters
     ```
   - 在右侧窗口中找到对应的键值（如 `MaxUserPort` 和 `TcpTimedWaitDelay`）。
   - 如果键值不存在，可以右键选择“新建” > “DWORD (32-bit) 值”，然后命名为对应的键名。

4. **设置参数值**：
   - 双击键值名称，在弹出的窗口中输入推荐值（如 `65534` 或 `30`），然后点击“确定”。

5. **重启计算机**：
   - 修改完成后，关闭注册表编辑器，并重启计算机以使更改生效。
