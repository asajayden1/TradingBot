class BSTNode:
    def __init__(self, price):
        self.price = price
        self.left = None
        self.right = None


class BST:
    """
    Binary Search Tree to store historical closing prices.
    Used to efficiently find min/max prices over a period,
    which helps contextualize whether current price is near
    a high or low — informing buy/sell decisions.
    """

    def __init__(self):
        self.root = None

    def insert(self, price):
        if self.root is None:
            self.root = BSTNode(price)
        else:
            self._insert(self.root, price)

    def _insert(self, node, price):
        if price < node.price:
            if node.left is None:
                node.left = BSTNode(price)
            else:
                self._insert(node.left, price)
        else:
            if node.right is None:
                node.right = BSTNode(price)
            else:
                self._insert(node.right, price)

    def get_min(self):
        """Returns the minimum price in the BST."""
        if self.root is None:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.price

    def get_max(self):
        """Returns the maximum price in the BST."""
        if self.root is None:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.price

    def search(self, price):
        """Returns True if a price exists in the BST."""
        return self._search(self.root, price)

    def _search(self, node, price):
        if node is None:
            return False
        if price == node.price:
            return True
        elif price < node.price:
            return self._search(node.left, price)
        else:
            return self._search(node.right, price)

    def build_from_prices(self, prices):
        """Inserts all prices from a list into the BST."""
        for price in prices:
            self.insert(price)


# test
if __name__ == "__main__":
    bst = BST()
    bst.build_from_prices([150, 145, 160, 138, 172, 155])
    print("Min price:", bst.get_min())   # 138
    print("Max price:", bst.get_max())   # 172
    print("Search 160:", bst.search(160))  # True
    print("Search 999:", bst.search(999))  # False