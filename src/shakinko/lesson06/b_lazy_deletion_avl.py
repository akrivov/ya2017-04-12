task = '''
Решите задачу A повторно, добавляя метод удаления узлов.
Метод del(key) должен реализовать "ленивое" удаление с коэффициентом обновления 0.5,
т.е. полное перестроение дерева производится когда количество удаленных узлов
становится равным или большим количества оставшихся в дереве.
'''


# ----------------------------------- ДЕРЕВО ------------------------------------
class AvlB():
    # ------------------------------- ОТДЕЛЬНЫЙ УЗЕЛ ------------------------------------
    class Node():
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.height = 0
            # С каждым узлом ассоциирован флаг deleted
            self.deleted = False

        def balance(self):
            return (self.left.height if self.left else -1) - (
                self.right.height if self.right else -1)

        def __str__(self):
            return str(self.key)

    def __init__(self, root=None):
        self.root = self.copy_tree = root  # 2 корня, тот, который copy нужен для lazy deletion
        self._outlist = list()  # вспомогательный лист в котором строится дерево для вывода его на экран
        # for lazy deletion
        self.nodecount = 0
        self.delcount = 0

    def free(self):
        if not self.root:
            return
        self._free(self.root)

    def add(self, key, value):
        self.root = self._add(self.root, key, value)

    def delete(self, key):
        # ищем узел
        self.lookup(key)
        # и просто включаем ему флаг deleted
        # print(t)
        self.deleted = True
        self.delcount += 1

        # коэффициент обновления = 0.5 хардкодим прямо здесь
        # по-хорошему его надо бы вынести в константы
        if self.nodecount * 0.5 <= self.delcount:
            # создаем новое дерево, содержащее все не удалённые узлы
            self.copy(self.root)
            # print(self.copy_tree)
            self.root = self.copy_tree       # копия встает на место оригинала
            self.nodecount -= self.delcount  # счетчик узлов уменьшился на кол-во удаленных узлов
            self.copy_tree = None            # уничтожаем копию
            self.delcount = 0

    def copy(self, node):
        if node:
            if not node.deleted:
                self.copy_tree = self._add(self.copy_tree, node.key, node.value)
                # print("key =", node.key)

            if node.left and not node.left.deleted:
                self.copy_tree = self._add(self.copy_tree, node.left.key, node.left.value)
                # print("left.key =", node.left.key)

            elif node.right and not node.right.deleted:
                self.copy_tree = self._add(self.copy_tree, node.right.key, node.right.value)
                # print("right.key =", node.right.key)

        # рекурсивно спускаемся по дереву и продолжаем копировать
            self.copy(node.left)
            self.copy(node.right)

    def lookup(self, key):
        return self._lookup(self.root, key)

    def _free(self, tree):
        if tree:
            self._free(tree.left)
            self._free(tree.right)
            self.nodecount = 0
            self.delcount = 0
            tree = None

    def _lookup(self, tree, key):
        while tree:
            if tree.key == key:
                return tree
            elif key < tree.key:
                tree = tree.left
            else:
                tree = tree.right
        return tree

    def _create(self, key, value):
        return self.Node(key, value)

    def _height(self, tree):
        return tree.height if tree else -1

    def _add(self, tree, key, value):
        if not tree:
            self.root = self._create(key, value)
            # Инкрементим счетчик, это нужно будет потом для lazy deletion
            self.nodecount += 1
            return self.root
        if (key < tree.key):
            tree.left = self._add(tree.left, key, value)
            if self._height(tree.left) - self._height(tree.right) == 2:
                if key < tree.left.key:
                    tree = self._right_rotate(tree)
                else:
                    tree = self._leftright_rotate(tree)
        elif (key > tree.key):
            tree.right = self._add(tree.right, key, value)
            if self._height(tree.right) - self._height(tree.left) == 2:
                if key > tree.right.key:
                    tree = self._left_rotate(tree)
                else:
                    tree = self._rightleft_rotate(tree)

        else:
            if tree.deleted:
                tree.deleted = False
                self.delcount -= 1
            else:
                tree.value = value
        tree.height = max(self._height(tree.left), self._height(tree.right)) + 1
        return tree

    def _right_rotate(self, tree):
        root = tree.left
        tree.left = root.right
        root.right = tree
        tree.height = max(self._height(tree.left), self._height(tree.right)) + 1
        root.height = max(self._height(root.left), tree.height) + 1
        return root

    def _left_rotate(self, tree):
        root = tree.right
        tree.right = root.left
        root.left = tree
        tree.height = max(self._height(tree.left), self._height(tree.right)) + 1
        root.height = max(self._height(root.right), tree.height) + 1
        return root

    def _leftright_rotate(self, tree):
        tree.left = self._left_rotate(tree.left)
        return self._right_rotate(tree)

    def _rightleft_rotate(self, tree):
        tree.right = self._right_rotate(tree.right)
        return self._left_rotate(tree)

    # обновление массива для строкового представления дерева
    def _dfs_print(self, tree, level):
        if level == 0:
            self._outlist = list()
        if len(self._outlist) < level + 1:
            self._outlist.append(" ")
        self._outlist[level] += (str(tree) if tree else ".") + " "
        if tree:
            self._dfs_print(tree.left, level + 1)
            self._dfs_print(tree.right, level + 1)

    # строковое представление дерева
    def __str__(self) -> str:
        self._dfs_print(self.root, 0)
        out = ""
        max = 0
        for s_Level in self._outlist:
            if len(s_Level) > max:
                max = len(s_Level)
        for s_Level in self._outlist:
            spaces = ""
            line = s_Level
            while (len(line) <= max):
                line = s_Level
                spaces += " "
                line = line.replace(" ", spaces)
            subspaces = " " * (len(spaces) - 1)
            while (len(line) > max):
                line = line.replace(spaces, subspaces, 1)
            if len(line.replace(".","").replace(" ",""))>0:
                out += line + "\n"
        out += "-"*max
        return out


# ------------------------ПРОВЕРКА РАБОТОСПОСОБНОСТИ -------------------------
def main():
    # чтение одной строки из файла
    def arr(filename):
        return filename.readline().replace("\n", "").split(" ")
    f = open("dataB.txt")
    count = int(arr(f)[0])
    avl = AvlB()
    keys=list()
    for i in range(0, count):
        data = arr(f)
        assert len(data) == 2
        avl.add(data[0], int(data[1]))
        keys.append(data[0])
    print(avl)
    print("Удаление половины узлов")
    for i in range(count//2, count):
        avl.delete(keys[i])
    print(avl)


# Для ручной проверки нажмите Ctrl+Shift+F10
# установив курсор на  main
# или создайте конфигурацию Run-Edit configuration
if __name__ == "__main__":
    main()
