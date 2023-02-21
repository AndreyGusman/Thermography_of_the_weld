// stdafx.h : include file for standard system include files,
//  or project specific include files that are used frequently, but
//      are changed infrequently
//

#if !defined(AFX_STDAFX_H__958D3DC0_9D67_48EC_9F87_E479F0E0C7BA__INCLUDED_)
#define AFX_STDAFX_H__958D3DC0_9D67_48EC_9F87_E479F0E0C7BA__INCLUDED_


#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#define VC_EXTRALEAN		// Exclude rarely-used stuff from Windows headers

#endif // _AFX_NO_AFXCMN_SUPPORT

#include <afxwin.h>         // MFC core and standard components
#include <afxext.h>         // MFC extensions
#include <afxdisp.h>        // MFC Automation classes
#include <afxdtctl.h>	
#include <afxcmn.h>			// MFC support for Windows Common Controls




//#include <afxcontrolbars.h>



	// MFC support for Internet Explorer 4 Common Controls
#ifndef _AFX_NO_AFXCMN_SUPPORT

//#define  USE_GBIT_DRIVER     1       //Ç§Õ×ÍøºÍ°ÙÕ×ÍøÇÐ»» 
//#include "resource.h"
#define  MAX_STRLEN   256 


#include "api.h"
//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.
char * _UnicodeStringToAnsic(CString str1);

#endif // !defined(AFX_STDAFX_H__958D3DC0_9D67_48EC_9F87_E479F0E0C7BA__INCLUDED_)

