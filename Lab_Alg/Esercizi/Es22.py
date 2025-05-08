class Node:
    def __init__(self, key: int, value: str):
        self.key = key
        self.value = value
        self.height = 1  # Ogni nodo parte con altezza 1
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key: int, value: str):
        """Inserimento di un nodo e ribilanciamento dell'albero"""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self.root = self._insert(self.root, key, value)

    def _insert(self, node: Node, key: int, value: str) -> Node:
        """Inserimento ricorsivo interno con bilanciamento"""
        if node is None:
            return Node(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value  # aggiorna il valore se la chiave esiste già
            return node

        # aggiorna altezza
        node.height = 1 + max(self._height(node.left), self._height(node.right))

        # ribilanciamento
        return self._balance(node)

    def remove(self, key: int):
        """Rimozione del nodo tramite chiave"""
        self.root = self._remove(self.root, key)

    def _remove(self, node: Node, key: int) -> Node:
        """Rimozione ricorsiva interna con bilanciamento"""
        if not node:
            return None

        # Naviga nell'albero
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            # Nodo trovato
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Due figli: trova il successore in-order
                successor = self._min_value_node(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = self._remove(node.right, successor.key)

        # Aggiorna altezza e ribilancia
        self._update_height(node)
        return self._balance(node)
    
    # ------------------------ FUNZIONI DI SUPPORTO ------------------------- #

    def _min_value_node(self, node: Node) -> Node:
        while node.left:
            node = node.left
        return node
    
    def _update_height(self, node: Node):
        """Aggiorna l'altezza del nodo corrente basandosi sui figli."""
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        node.height = 1 + max(left_height, right_height)
    # _______________________________________________________________________ #

    def find(self, key: int) -> str:
        """Ricerca del valore associato alla chiave"""
        result = self._find(self.root, key)
        print(result if result is not None else "NOT FOUND")

    def _find(self, node: Node, key: int) -> str:
        """Ricerca ricorsiva"""
        if not node:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def clear(self):
        """Reset dell'albero"""
        self.root = None

    def show(self):
        """Mostra l'albero"""
        print(self._preorder(self.root))

    def _preorder(self, node: Node) -> str:
        """Costruzione stringa ricorsivamente in forma polacca"""
        if node is None:
            return "NULL"

        current = f"{node.key}:{node.value}:{node.height}"
        left = self._preorder(node.left)
        right = self._preorder(node.right)

        return f"{current} {left} {right}"

    def _height(self, node: Node) -> int:
        """Restituisce l'altezza del nodo"""
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node: Node) -> int:
        """Restituisce il fattore di bilanciamento"""
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, x: Node) -> Node:
        """Rotazione a sinistra"""
        y = x.right
        T2 = y.left

        # rotazione
        y.left = x
        x.right = T2

        # aggiorna altezze
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y  # y nuova radice del sottoalbero

    def _rotate_right(self, y: Node) -> Node:
        """Rotazione a destra"""
        x = y.left
        T2 = x.right

        # rotazione
        x.right = y
        y.left = T2

        # aggiorna altezze
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))

        return x  # x nuova radice del sottoalbero

    def _balance(self, node: Node) -> Node:
        """Rotazioni necessarie per bilanciare il nodo"""
        balance = self._get_balance(node)

        # sinistra pesante
        if balance > 1:
            if self._get_balance(node.left) >= 0:
                return self._rotate_right(node)  # caso LL
            else:
                node.left = self._rotate_left(node.left)  # caso LR
                return self._rotate_right(node)

        # destra pesante
        if balance < -1:
            if self._get_balance(node.right) <= 0:
                return self._rotate_left(node)  # caso RR
            else:
                node.right = self._rotate_right(node.right)  # caso RL
                return self._rotate_left(node)

        return node

def interactive_loop():
    """Ciclo interattivo per eseguire i comandi"""
    tree = AVLTree()
    while True:
        try:
            command = input("> ").strip()
            if command.startswith("insert "):
                _, key, value = command.split(maxsplit=2)
                tree.insert(int(key), value)
            elif command.startswith("remove "):
                _, key = command.split(maxsplit=1)
                tree.remove(int(key))
            elif command.startswith("find "):
                _, key = command.split(maxsplit=1)
                tree.find(int(key))
            elif command == "clear":
                tree.clear()
            elif command == "show":
                tree.show()
            else:
                break
        except Exception as e:
            print(f"Errore: {e}")

if __name__ == "__main__":
    interactive_loop()