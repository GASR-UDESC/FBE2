IF R.active THEN
	reset();
	RO.active := True;
ELSE 
	RO.active := False;
END_IF;

IF CU.active THEN
	counter();
	CUO.active := True;
ELSE
	CUO.active := False;
END_IF;
