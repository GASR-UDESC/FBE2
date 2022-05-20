IF EI.active THEN
	IF K.value = 0 THEN
		EO0.active := True;	
		EO1.active := False;
		EO2.active := False;
		EO3.active := False;
	ELSIF K.value = 1 THEN
		EO0.active := False;	
		EO1.active := True;
		EO2.active := False;
		EO3.active := False;
	ELSIF K.value = 2 THEN
		EO0.active := False;	
		EO1.active := False;
		EO2.active := True;
		EO3.active := False;
	ELSIF K.value = 3 THEN
		EO0.active := False;	
		EO1.active := False;
		EO2.active := False;
		EO3.active := True;
	END_IF;
END_IF;
