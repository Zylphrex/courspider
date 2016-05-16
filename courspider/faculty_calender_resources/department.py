class Department:

    def __init__(self, name):
        """
        Represents a department

        :param name: the name of the department
        :type name: string
        """
        self.name = name

    def __str__(self):
        return self.name
        
    def __eq__(self, other):
        """
        Returns True if this Department is equal to other.

        They are equal if and only if other is an instance of a Department, and
        both departments have the same name

        :param other: The other object to compare to
        :type other: Object
        :return: whether or not these they are equal
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False
