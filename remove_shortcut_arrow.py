import winreg
import subprocess
import sys
def restart_explorer ():
    try :
        subprocess .run (['taskkill','/F','/IM','explorer.exe'],
        capture_output =True ,check =False )
        subprocess .Popen ('explorer.exe')
        return True
    except Exception as e :
        print (f"Ошибка при перезапуске проводника: {e }")
        return False
def remove_arrow ():
    try :
        key_path =r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons"
        key =winreg .CreateKey (winreg .HKEY_LOCAL_MACHINE ,key_path )
        winreg .SetValueEx (key ,"29",0 ,winreg .REG_SZ ,"")
        winreg .CloseKey (key )
        print ("✓ Стрелка успешно убрана!")
        print ("\n⚠️  Необходимо перезапустить проводник для применения изменений.")
        response =input ("\nПерезапустить проводник сейчас? (y/n): ").lower ()
        if response =='y':
            print ("\nПерезапускаю проводник...")
            restart_explorer ()
            print ("✓ Готово! Проверьте рабочую область.")
        else :
            print ("\n⚠️  Не забудьте перезапустить проводник вручную или перезагрузить компьютер.")
        return True
    except PermissionError :
        print ("❌ Ошибка: Недостаточно прав для изменения реестра.")
        print ("   Запустите программу от имени администратора!")
        return False
    except Exception as e :
        print (f"❌ Ошибка: {e }")
        return False
def restore_arrow ():
    try :
        key_path =r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons"
        try :
            key =winreg .OpenKey (winreg .HKEY_LOCAL_MACHINE ,key_path ,0 ,winreg .KEY_WRITE )
            try :
                winreg .DeleteValue (key ,"29")
                print ("✓ Параметр 29 удален из реестра.")
            except FileNotFoundError :
                print ("ℹ️  Параметр 29 не найден (возможно, уже удален).")
            winreg .CloseKey (key )
            try :
                key =winreg .OpenKey (winreg .HKEY_LOCAL_MACHINE ,key_path ,0 ,winreg .KEY_READ )
                try :
                    i =0
                    while True :
                        winreg .EnumValue (key ,i )
                        i +=1
                except OSError :
                    pass
                winreg .CloseKey (key )
                if i ==0 :
                    response =input ("\nРаздел Shell Icons пуст. Удалить его полностью? (y/n): ").lower ()
                    if response =='y':
                        key =winreg .OpenKey (winreg .HKEY_LOCAL_MACHINE ,
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer",
                        0 ,winreg .KEY_WRITE )
                        winreg .DeleteKey (key ,"Иконки оболочки")
                        winreg .CloseKey (key )
                        print ("✓ Раздел Shell Icons удален.")
            except :
                pass
        except FileNotFoundError :
            print ("ℹ️  Раздел Shell Icons не найден (стрелки уже восстановлены).")
            return True
        print ("\n✓ Стрелки будут восстановлены после перезапуска проводника.")
        response =input ("\nПерезапустить проводник сейчас? (y/n): ").lower ()
        if response =='y':
            print ("\nПерезапускаю проводник...")
            restart_explorer ()
            print ("✓ Готово! Стрелки должны вернуться.")
        else :
            print ("\n⚠️  Не забудьте перезапустить проводник вручную или перезагрузить компьютер.")
        return True
    except PermissionError :
        print ("❌ Ошибка: Недостаточно прав для изменения реестра.")
        print ("   Запустите программу от имени администратора!")
        return False
    except Exception as e :
        print (f"❌ Ошибка: {e }")
        return False
def check_admin ():
    try :
        import ctypes
        return ctypes .windll .shell32 .IsUserAnAdmin ()!=0
    except :
        return False
def main ():
    print ("="*60 )
    print ("  Удаление стрелок с ярлыков на рабочем столе Windows")
    print ("="*60 )
    print ()
    if not check_admin ():
        print ("⚠️  ВНИМАНИЕ: Программа должна быть запущена от имени администратора!")
        print ("   Для изменения реестра требуются права администратора.")
        print ()
        response =input ("Продолжить все равно? (y/n): ").lower ()
        if response !='y':
            print ("Программа завершена.")
            return
        print ()
    while True :
        print ("\nВыберите действие:")
        print ("1. Убрать стрелку")
        print ("2. Восстановить стрелки")
        print ("3. Выход")
        print ()
        choice =input ("Ваш выбор (1-3): ").strip ()
        if choice =='1':
            print ("\n"+"-"*60 )
            remove_arrow ()
            print ("-"*60 )
        elif choice =='2':
            print ("\n"+"-"*60 )
            restore_arrow ()
            print ("-"*60 )
        elif choice =='3':
            print ("\nДо свидания!")
            break
        else :
            print ("\n❌ Неверный выбор. Попробуйте снова.")
if __name__ =="__main__":
    try :
        main ()
    except KeyboardInterrupt :
        print ("\n\nПрограмма прервана пользователем.")
        sys .exit (0 )
    except Exception as e :
        print (f"\n❌ Критическая ошибка: {e }")
        sys .exit (1 )