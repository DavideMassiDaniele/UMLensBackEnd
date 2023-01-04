# metrica per individuare la lifeline meno coinvolta del diagramma (in termini di messaggi inviati e ricevuti)
def _lessUsedAbstraction(self):
    lifelines = self._parse_lifelines();
    ll = self._ll_id_list()
    _n = {}
    for i in lifelines:
        _n[i.get('ID')] = ll.count(i.get('ID'))
        m = min(_n, key=_n.get)
        min_ll = {m : _n[m]}   
    return min_ll

# metrica per individuare la lifeline più coinvolta del diagramma (in termini di messaggi inviati e ricevuti)
def _multifacedAbstraction(self):
    lifelines = self._parse_lifelines();
    ll = self._ll_id_list()
    _n = {}
    for i in lifelines:
        _n[i.get('ID')] = ll.count(i.get('ID'))
        m = max(_n, key=_n.get)
        max_ll = {m : _n[m]}   
    return max_ll

# metrica per individuare un'eventuale lifeline priva di interazioni con il diagramma
def _unutilizedAbstraction(self):
    lifelines = self._parse_lifelines();
    ll = self._ll_id_list()
    _n = {}
    for i in lifelines:
        _n[i.get('ID')] = ll.count(i.get('ID'))
    for key, value in _n.items():
        if value == 0:
            return key

# metrica per identificare i messaggi duplicati nel diagramma
def _duplicateMessages(self):
    messages = self._parse_messages()
    M = []
    for m in messages:
        M.append(m.get('NAME'))
    dup = {x for x in M if M.count(x) > 1}
    return dup