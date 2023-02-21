// stdafx.cpp : source file that includes just the standard includes
//	Demo1.pch will be the pre-compiled header
//	stdafx.obj will contain the pre-compiled type information

#include "stdafx.h"



char * _UnicodeStringToAnsic(CString str1)
{
#ifdef _UNICODE

	int len = WideCharToMultiByte(CP_ACP, 0, str1, -1, NULL, 0, NULL, NULL);
	char *ptxtTemp = new char[len + 1];
	WideCharToMultiByte(CP_ACP, 0, str1, -1, ptxtTemp, len, NULL, NULL);

#else 
	int len = str1.GetLength();
	char *ptxtTemp = new char[len + 1];

	// 	strncpy(ptxtTemp, str1.GetBuffer( 0 ), str1.GetLength() );        // ???????????

	strcpy(ptxtTemp, str1.GetBuffer(0));

	str1.ReleaseBuffer(); //千万不能缺少

#endif 




	return ptxtTemp;
}
