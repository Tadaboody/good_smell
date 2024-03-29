#: Warn when using join on a list of known literals.
# join-literal
a = "foo"
b = "bar"
",".join([a, b])
# ==>
a = "foo"
b = "bar"
"{},{}".format(a, b)
# END
#: Don't warn when joining an iterable
# None
iterable = ["a","b"]
",".join(iterable)
# ==>
iterable = ["a","b"]
",".join(iterable)
# END
#: Don't warn when joining a generator expression
# None
",".join(str(i) for i in range(100))
# ==>
",".join(str(i) for i in range(100))
# END
#: Don't warn when joining a list comprehension
# None
",".join([str(i) for i in range(100)])
# ==>
",".join([str(i) for i in range(100)])
# END
#: Don't warn when the list literal includes an unpacking
# None
",".join([1,2,3,*a])
# ==>
",".join([1,2,3,*a])
# END