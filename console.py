#!/usr/bin/python3
"""
console module
"""
import cmd
import re
import sys
import json
from shlex import split
# from models import base_model
# from models import user
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.city import City


class HBNBCommand(cmd.Cmd):
    """
    Creates the console interpreter for AirBnB project
    """
    prompt = '(hbnb) '

    def type_parser(self, token):
        """
        Returns the attribute value according to the given type
        """
        if token.isalpha():
            return str(token)
        if token.isdigit():
            return int(token)
        if re.search('[a-zA-Z]', token) and re.search('[0-9]', token):
            return str(token)
        if (token.startswith("'") and token.endswith("'")):
            word = token.strip("'")
            return str(word)
        if (token.startswith('"') and token.endswith('"')):
            word = token.strip('"')
            return str(word)
        if '.' in token:
            return float(token)
        return token

    def update_dictionary_loader(self, token):
        """
        Checks if a dictionary has been passed as an
        argument to the update method.
        If true adds the data to the object.
        Else the update method continues with the operation
        """
        if '{' in token and '}' in token:
            args = token.split(' ', maxsplit=2)
            dict_str = args[2].replace("'", '"')
            tmp_dict = json.loads(dict_str)

            try:
                my_class = globals()[args[0]]
            except Exception:
                print("** class name missing **")
            try:
                classname = getattr(my_class, '__name__')
            except Exception:
                print("** class doesn't exist **")
                return

            key1 = classname + '.' + args[1]
            for key, obj in storage.all().items():
                if key == key1:
                    for key, value in tmp_dict.items():
                        key_str = str(key)
                        attr_val = value
                        setattr(obj, key_str, attr_val)
                    storage.save()
                    storage.reload()
                    break
            return True
        return False

    def add_quotes(self, token):
        """
        Protects the token's type from being altered
        (by the type_parser class method) if called from
        the Default class method
        """
        if type(token) == str:
            if token.isdigit():
                word = '"' + token + '"'
                return word
            if re.match(r'^\d+\.\d+$', token):
                word = '"' + token + '"'
                return word
        return token

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        EOF signal to exit the program
        """
        return True

    def emptyline(self):
        """
        An empty line + ENTER shouldn’t execute anything
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        Usage: <class name>.create()
               create <class name>
        """
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if hasattr(sys.modules[__name__], args[0]):
            cls = getattr(sys.modules[__name__], args[0])
        else:
            print("** class doesn't exist **")
            return

        obj = cls()
        obj.save()
        storage.reload()
        print(obj.id)

    def do_show(self, arg):
        """
        Prints the string representation of an
        instance based on the class name and id.
        Usage: <class name>.show(<id>)
               show <class name> <id>
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        try:
            my_class = globals()[args[0]]
            classname = getattr(my_class, '__name__')
        except Exception:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key1 = classname + '.' + obj_id
        if key1 not in storage.all():
            print("** no instance found **")
            return
        for key, value in storage.all().items():
            if key == key1:
                obj = value
                print(obj)

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name
        and id (save the change into the JSON file).
        Usage: <class name>.destroy(<id>)
               destroy <class name> <id>
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        try:
            my_class = globals()[args[0]]
            classname = getattr(my_class, '__name__')
        except Exception:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key1 = classname + '.' + obj_id
        if key1 not in storage.all():
            print("** no instance found **")
            return
        for key, obj in storage.all().items():
            if key == key1:
                del storage.all()[key]
                storage.save()
                storage.reload()
                break

    def do_all(self, line):
        """
        Prints all string representations of
        instances of a class if no argument is given
        else prints string representation of instances
        of the given class
        Usage: <all>
               <class name>.all()
        """
        class_name = line.strip()
        objects = storage.all()
        if not class_name:
            obj_list = [str(obj) for obj in objects.values()]
            print(obj_list)
        else:
            try:
                my_class = globals()[class_name]
                classname = getattr(my_class, '__name__')
            except Exception:
                print("** class doesn't exist **")
                return
            print([
                str(obj)
                for obj in objects.values()
                if obj.__class__.__name__ == class_name
                ])

    def do_update(self, arg):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute (save the
        change into the JSON file)
        Usage: update <class name> <id> <attribute name> <attribute value>
               <class name>.update(<id>, <attribute name>, <attribute value>)
               <class name> <id> <dictionary representation>
               <class name>.update(<id>, <dictionary representation>
        """
        if not arg:
            print("** class name missing **")
            return
        if self.update_dictionary_loader(arg):
            return
        args = arg.split()
        try:
            my_class = globals()[args[0]]
            classname = getattr(my_class, '__name__')
        except Exception:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key1 = classname + '.' + obj_id
        if key1 not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        for key, obj in storage.all().items():
            if key == key1:
                new_value = self.type_parser(args[3])
                setattr(obj, args[2], new_value)
                storage.save()
                storage.reload()
                break

    def do_count(self, arg):
        """
        Counts the number of instances of a class
        Usage: count <class name>
               <class name>.count()
        """
        storage.reload()
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        try:
            my_class = globals()[args[0]]
            classname = getattr(my_class, '__name__')
        except Exception:
            print("0")
            return
        objects = storage.all()
        count = 0
        for key in objects.keys():
            if args[0] in key:
                count += 1
        print("{}".format(count))

    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
        """
        argdict = {
                "create": self.do_create,
                "all": self.do_all,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "count": self.do_count,
                "update": self.do_update
                }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if not argl[0] and argl[1] != "all()":
                print("** class name missing **")
                return
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] == 'update' and \
                        '{' in command[1] and \
                        '}' in command[1]:
                    cmd_str = command[1].split(', ', maxsplit=1)
                    dict_str = cmd_str[1].replace("'", "\"")
                    try:
                        d_dict = json.loads(dict_str)
                    except Exception:
                        return
                    for key, value in d_dict.items():
                        k_str = str(key)
                        v_str = self.add_quotes(value)
                        call = "{} {} {} {}".format(
                                argl[0], cmd_str[0],
                                k_str, v_str
                                )
                        argdict[command[0]](call)
                    return

                elif command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    call = re.sub(r',', '', call)
                    return argdict[command[0]](call)

        print("*** Unknown syntax: {}".format(arg))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
