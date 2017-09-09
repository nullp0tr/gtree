charset = [
    '│',

    '└',
    '─',
    '├',
    '┬',
]


def tree(nodes_list, children_property=None, extra_children_properties=None,
         addtoprefix=None, _level=0, _node_index=0, _level_meta=(),
         indent=3, _output_tree=None):
    if _output_tree is None:
        _output_tree = []
    back_up_list = tuple(nodes_list)
    list_size = len(nodes_list)

    for obj in back_up_list:
        prefix = ' ' * _level * indent
        if _level_meta:
            rlevel_meta = _level_meta[::-1]
            for meta_tupe in rlevel_meta:
                lvl, nindex, lsize = meta_tupe
                if _level > 1 and _level > lvl > 0:
                    if nindex == lsize - 1:
                        prefix = prefix[:lvl * indent] + ' ' + prefix[lvl * indent + 1:]
                    else:
                        prefix = prefix[:lvl * indent] + charset[0] + prefix[lvl * indent + 1:]

        children = []
        if extra_children_properties is not None:
            extra_children_property = []
            for property_ in extra_children_properties:
                try:
                    extra_children_property += [getattr(obj, property_)]
                except AttributeError:
                    if not extra_children_property:
                        extra_children_property = []
                finally:
                    children = extra_children_property

        if children_property is not None:
            try:
                children_getter = getattr(obj, children_property)
                obj_children = children_getter()
            except AttributeError:
                obj_children = []
            finally:
                children += obj_children

        children_size = 0
        if children is not None:
            children_size = len(children)

        if _level == 0:
            prefix = prefix + charset[2]
        elif _node_index == list_size - 1:
            prefix = prefix + charset[1]
        else:
            prefix = prefix + charset[3]

        if children_size > 0:
            prefix = prefix + (charset[2] * indent)[:-1] + charset[4]
        else:
            prefix = prefix + charset[2] * indent

        tobeadded = ''
        if addtoprefix is not None:
            tobeadded = addtoprefix(level=_level)

        line = str(obj)
        _output_tree.append((prefix + tobeadded, line, obj))
        if children_size > 0:
            _level_meta = ((_level, _node_index, list_size),) + _level_meta
            tree(children, _level=_level + 1, _level_meta=_level_meta, _output_tree=_output_tree,
                 children_property=children_property, extra_children_properties=extra_children_properties,
                 addtoprefix=addtoprefix)
        _node_index += 1

    return _output_tree


def print_tree(nodes_tree):
    for node in nodes_tree:
        prefix, line, _ = node
        print(prefix + ' ' + line)
