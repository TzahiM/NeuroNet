Description
-----------

Parses iCalendar and vCard files into Python data structures, decoding the
relevant encodings. Also serializes vobject data structures to iCalendar, vCard,
or (experimentally) hCalendar unicode strings.

Requirements
------------

Requires python 2.7 or later, dateutil 2.4.0 or later.

Recent changes
--------------
   - Make ics_diff.py work with Python 3
   - Huge changes to text encoding for Python 2/3 compatibility
   - Autogenerate DTSTAMP if not provided
   - Fix getrruleset() for Python 3 and in the case that addRDate=True
   - Update vCard property validation to match specifications
   - Handle offset-naive and offset-aware datetimes in recurrence rules
   - Improved documentation for multi-value properties

For older changes, see
   - http://eventable.github.io/vobject/#release-history or
   - http://vobject.skyhouseconsulting.com/history.html

