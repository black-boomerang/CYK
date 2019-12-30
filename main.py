class Rule:
    def __init__(self, string_rule):
        self.first_part, self.second_part = string_rule.strip().split("->")


class Grammar:
    def __init__(self, rules=()):
        self.symbols = set()
        self.nonterminals = set()
        self.rules = []
        sz = 0
        for rule in rules:
            self.rules.append(Rule(rule))
            self.nonterminals.update(self.rules[sz].first_part)
            nonterms = set(self.rules[sz].second_part)
            nonterms = {x for x in nonterms if x.isupper()}
            self.nonterminals.update(nonterms)
            self.symbols.update(self.rules[sz].first_part)
            self.symbols.update(self.rules[sz].second_part)
            sz += 1
        self.start_symbol = self.rules[0].first_part if sz > 0 else '0'

    def copy(self):
        new_grammar = Grammar()
        new_grammar.start_symbol = self.start_symbol
        new_grammar.symbols = self.symbols.copy()
        new_grammar.nonterminals = self.nonterminals.copy()
        return new_grammar


class Algo:
    def __init__(self):
        self.grammar = Grammar()

    def find_next_nonterminal_ord(self, cur_nonterminal_ord, symbols):
        while chr(cur_nonterminal_ord) in symbols:
            cur_nonterminal_ord += 1
        return cur_nonterminal_ord

    def remove_long_rules(self, grammar: Grammar):
        new_grammar = grammar.copy()
        cur_nonterminal_ord = ord('A')
        for rule in grammar.rules:
            if len(rule.second_part) > 2:
                nonterminal = rule.first_part[0]
                for i in range(len(rule.second_part) - 2):
                    cur_nonterminal_ord = self.find_next_nonterminal_ord(
                        cur_nonterminal_ord, new_grammar.symbols)
                    new_grammar.rules.append(Rule(
                        nonterminal + '->' + rule.second_part[i] + chr(
                            cur_nonterminal_ord)))
                    new_grammar.symbols.add(chr(cur_nonterminal_ord))
                    new_grammar.nonterminals.add(chr(cur_nonterminal_ord))
                    nonterminal = chr(cur_nonterminal_ord)
                new_grammar.rules.append(Rule(
                    nonterminal + '->' + rule.second_part[
                        len(rule.second_part) - 2] +
                    rule.second_part[len(rule.second_part) - 1]))
            else:
                new_grammar.rules.append(rule)
        return new_grammar

    def remove_eps_rules(self, grammar: Grammar):
        is_epsilon = dict.fromkeys(grammar.symbols, False)
        containing_rules = {x: set() for x in grammar.nonterminals}
        checked_num = [len(rule.second_part) for rule in grammar.rules]
        sz = len(grammar.rules)
        for i in range(sz):
            for symbol in grammar.rules[i].second_part:
                if symbol in grammar.nonterminals:
                    containing_rules[symbol].add(i)

        nonterminals_queue = []
        for i in range(sz):
            if grammar.rules[i].second_part == '1':
                nonterminals_queue.append(grammar.rules[i].first_part)

        while len(nonterminals_queue) != 0:
            cur_nonterminal = nonterminals_queue.pop(0)
            if is_epsilon[cur_nonterminal]:
                continue
            is_epsilon[cur_nonterminal] = True
            for rule_num in containing_rules[cur_nonterminal]:
                checked_num[rule_num] -= 1
                if checked_num[rule_num] == 0:
                    nonterminals_queue.append(
                        grammar.rules[rule_num].first_part)

        new_grammar = grammar.copy()
        if is_epsilon[grammar.start_symbol]:
            new_grammar.rules.append(Rule(grammar.start_symbol + '->1'))
        for rule in grammar.rules:
            second_part = rule.second_part
            if second_part != '1':
                new_grammar.rules.append(rule)
            if len(second_part) < 2:
                continue
            if is_epsilon[second_part[0]]:
                new_grammar.rules.append(
                    Rule(rule.first_part + '->' + second_part[1]))
            if is_epsilon[second_part[1]]:
                new_grammar.rules.append(
                    Rule(rule.first_part + '->' + second_part[0]))
        return new_grammar

    def remove_unit_rules(self, grammar: Grammar):
        inferred_rules = {x: set() for x in grammar.nonterminals}
        for rule in grammar.rules:
            inferred_rules[rule.first_part].add(rule.second_part)
        for i in range(len(grammar.rules)):
            for rule in grammar.rules:
                if rule.second_part in grammar.nonterminals:
                    inferred_rules[rule.first_part].update(
                        inferred_rules[rule.second_part])

        new_grammar = grammar.copy()
        for nonterminal, inferred_set in inferred_rules.items():
            for second_part in inferred_set:
                if second_part not in new_grammar.nonterminals:
                    new_grammar.rules.append(
                        Rule(nonterminal + '->' + second_part))
        return new_grammar

    def remove_nongenerating_rules(self, grammar: Grammar):
        generating_rules = set()
        for i in range(len(grammar.rules)):
            for rule in grammar.rules:
                is_generating = True
                for symbol in rule.second_part:
                    if symbol in grammar.nonterminals and \
                            symbol not in generating_rules:
                        is_generating = False
                if is_generating:
                    generating_rules.add(rule.first_part)

        new_grammar = grammar.copy()
        new_grammar.nonterminals = generating_rules
        for rule in grammar.rules:
            is_generating = True if rule.first_part in generating_rules else False
            for symbol in rule.second_part:
                if symbol in grammar.nonterminals and \
                        symbol not in generating_rules:
                    is_generating = False
            if is_generating:
                new_grammar.rules.append(rule)
        return new_grammar

    def remove_unreachable_rules(self, grammar: Grammar):
        reachable_rules = set(grammar.start_symbol)
        for i in range(len(grammar.rules)):
            for rule in grammar.rules:
                if rule.first_part not in reachable_rules:
                    continue
                for symbol in rule.second_part:
                    if symbol in grammar.nonterminals:
                        reachable_rules.add(symbol)

        new_grammar = grammar.copy()
        new_grammar.nonterminals = reachable_rules
        for rule in grammar.rules:
            if rule.first_part in reachable_rules:
                new_grammar.rules.append(rule)
        return new_grammar

    def remove_wrong_rules(self, grammar: Grammar):
        new_grammar = grammar.copy()
        cur_nonterminal_ord = ord('A')
        for rule in grammar.rules:
            if len(rule.second_part) < 2:
                new_grammar.rules.append(rule)
            else:
                new_rule = ''
                for i in range(2):
                    if rule.second_part[i] not in grammar.nonterminals:
                        cur_nonterminal_ord = self.find_next_nonterminal_ord(
                            cur_nonterminal_ord, new_grammar.symbols)
                        new_grammar.symbols.add(chr(cur_nonterminal_ord))
                        new_grammar.nonterminals.add(chr(cur_nonterminal_ord))
                        new_rule += chr(cur_nonterminal_ord)
                        new_grammar.rules.append(
                            Rule(new_rule[i] + '->' + rule.second_part[i]))
                    else:
                        new_rule += rule.second_part[i]
                new_grammar.rules.append(
                    Rule(rule.first_part + '->' + new_rule))
        return new_grammar

    def fit(self, grammar: Grammar):
        new_grammar = self.remove_long_rules(grammar)
        new_grammar = self.remove_eps_rules(new_grammar)
        new_grammar = self.remove_unit_rules(new_grammar)
        new_grammar = self.remove_nongenerating_rules(new_grammar)
        new_grammar = self.remove_unreachable_rules(new_grammar)
        self.grammar = self.remove_wrong_rules(new_grammar)

    def predict(self, word):
        size = len(word)
        grammar = self.grammar
        inferred_rules = {x: set() for x in grammar.nonterminals}
        for rule in grammar.rules:
            inferred_rules[rule.first_part].add(rule.second_part)

        if word == '1':
            return '1' in inferred_rules[grammar.start_symbol]

        inferred = {x: [[False] * size for x in range(size)] for x in
                    grammar.nonterminals}
        for nonterminal in grammar.nonterminals:
            for j in range(size):
                if word[j] in inferred_rules[nonterminal]:
                    inferred[nonterminal][j][j] = True
        for subword_size in range(1, size):
            for nonterminal in grammar.nonterminals:
                for second_part in inferred_rules[nonterminal]:
                    if len(second_part) > 1:
                        for i in range(size - subword_size):
                            for j in range(i, i + subword_size):
                                if inferred[second_part[0]][i][j] and \
                                        inferred[second_part[1]][j + 1][
                                            i + subword_size]:
                                    inferred[nonterminal][i][
                                        i + subword_size] = True

        return inferred[grammar.start_symbol][0][size - 1]


def is_in_grammar(rules, word):
    grammar = Grammar(rules)
    algo = Algo()
    algo.fit(grammar)
    return algo.predict(word)


if __name__ == "__main__":
    n = int(input())
    rules = []
    for i in range(n):
        rules.append(input())
    word = input()
    print(is_in_grammar(rules, word))

