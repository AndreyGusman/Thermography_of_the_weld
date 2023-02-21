// Gradient.h: interface for the CColorPalleteDataMgr class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(__COLOR_PALLETE__)
#define __COLOR_PALLETE__

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include <afxtempl.h>


#define  MAX_PEG_NUM       15 
#define  MAX_PEGC_NUM      5 

	enum InterpolationMethod
	{
		Linear,
		FlatStart,
		FlatEnd,
		Reverse
	};

//#pragma pack(push, 8)  // CHANGE 1 TO 8

struct peginfo
{
	COLORREF color;
	float    posi; 
};

struct pegCinfo
{
	peginfo up ;
	peginfo down; 
	InterpolationMethod method; 
};


typedef  struct tagPALSRC{
	COLORREF backgroundcolor;
	COLORREF startpegcolor;
	COLORREF endpegcolor;
	BOOL busebackground;
	int  quantization;
	InterpolationMethod method;
	int pegcount;
	peginfo pegdata[MAX_PEG_NUM];  // 
	int pegCcount;
	pegCinfo pegCdata[MAX_PEGC_NUM] ; // 5 不能随便改 下位机决定的 
}PALLETE_DATA; 

//#pragma pack(pop)


class  AFX_CLASS_EXPORT CPeg : CObject
{
public:
	CPeg() ;
	CPeg(const CPeg &src) {colour = src.colour, position = src.position, id = src.id;};
	CPeg& operator = (const CPeg &src) {colour = src.colour, position = src.position, id = src.id; return *this;};
	void SerializeM(peginfo &ar,bool bload);
	const UINT GetID() const {return id;};


	COLORREF colour;
	float position;
protected:
	UINT id;
};


class  AFX_CLASS_EXPORT CCouplePeg : CObject
{
public:
	CCouplePeg() ;
	CCouplePeg(const CCouplePeg &src) {down = src.down, up = src.up, id = src.id, meathod = src.meathod ;};
	CCouplePeg& operator = (const CCouplePeg &src) {down = src.down, up = src.up, id = src.id, meathod = src.meathod ; return *this;};

	void SerializeM(pegCinfo &ar,bool bload);
	const UINT GetID() const {return id;};


	CPeg up, down ; 
	InterpolationMethod meathod; 
protected:
	UINT id;
};


#define BACKGROUND -4
#define STARTPEG -3
#define ENDPEG -2
#define NONE -1

typedef COLORREF (__cdecl* InterpolateFn)(COLORREF first, COLORREF second, float position, float start, float end);

class AFX_CLASS_EXPORT CColorPalleteDataMgr : public CObject  
{
public:
	CColorPalleteDataMgr();
	CColorPalleteDataMgr(CColorPalleteDataMgr &gradient);
	virtual ~CColorPalleteDataMgr();

	CColorPalleteDataMgr& operator =(CColorPalleteDataMgr &src);
	

//----- Attributes -----//
	int GetPegCount() const;
	const CPeg GetPeg(int iIndex) const;

	int SetPeg(int iIndex, COLORREF crColour, float fPosition);
	int SetPeg(int iIndex, CPeg peg);
	int AddPeg(COLORREF crColour, float fPosition);
	int AddPeg(CPeg peg);
	void RemovePeg(int iIndex);
	int IndexFromPos(float pos);

///
	int AddPegCouple(COLORREF crColour0, float fPosition0, 
									   COLORREF crColour1, float fPosition1,  InterpolationMethod meathod );
	void RemovePegCouple(int iIndex);
	int GetPegCoupleCount() const ;

	const CCouplePeg GetPegCouple(int iIndex) const;
	int SetPegCouple(int iIndex, COLORREF crColour0, float fPosition0, 
									   COLORREF crColour1, float fPosition1,  InterpolationMethod meathod);
	InterpolationMethod GetCoupleInterpolationMethod(int iIndex) const;
	void SetCoupleInterpolationMethod(int iIndex,const InterpolationMethod method);

	
///
	void SetStartPegColour(const COLORREF crColour){m_StartPeg.colour = crColour;};
	COLORREF GetStartPegColour() const {return m_StartPeg.colour;};
	void SetEndPegColour(const COLORREF crColour) {m_EndPeg.colour = crColour;};
	COLORREF GetEndPegColour() const {return m_EndPeg.colour;};

	void SetBackgroundColour(const COLORREF crColour) {m_Background.colour = crColour;};
	COLORREF GetBackgroundColour() const {return m_Background.colour;};
	void SetUseBackground(const BOOL bUseBackground) {m_UseBackground = bUseBackground;};
	BOOL GetUseBackground() const {return m_UseBackground;};
	
	InterpolationMethod GetInterpolationMethod() const;
	void SetInterpolationMethod(const InterpolationMethod method);

	int GetQuantization() const;
	void SetQuantization(const int entries);

//----- Operations -----//
	void MakePalette(RGBQUAD *lpPalette);
	
	void MakePalette(CPalette *lpPalette);
	void Make8BitPalette(RGBTRIPLE *lpPal);
	void MakeEntries(RGBTRIPLE *lpPal, int iEntryCount);

	void MakeCoupleEntries(RGBTRIPLE *lpPal, int iEntryCount);

	
	COLORREF ColourFromPosition(float pos);
	
	void SerializeM(PALLETE_DATA &ar,bool bload);

//----- Internals -----//
protected:
	void SortPegs();
	
	//----- Interpolation routines -----//
	static COLORREF InterpolateLinear(COLORREF first, COLORREF second,
		float position, float start, float end);
	static COLORREF InterpolateFlatStart(COLORREF first, COLORREF second,
		float position, float start, float end);
	static COLORREF InterpolateFlatEnd(COLORREF first, COLORREF second,
		float position, float start, float end);
	static COLORREF InterpolateReverse(COLORREF first, COLORREF second,
		float position, float start, float end);
private:	
	int IndexFromId(UINT id);
	void InsertSort(int lb, int ub);
	int Partition(int lb, int ub);
	void QuickSort(int lb, int ub);

protected:
	InterpolateFn GetInterpolationProc();
	InterpolateFn GetInterpolationProc( InterpolationMethod in );
	POSITION GetNextPeg(POSITION current);
	
	CArray <CPeg, CPeg&> pegs;

	CArray <CCouplePeg, CCouplePeg&> couplepegs;  //add 

	CPeg m_StartPeg, m_EndPeg, m_Background;
	BOOL m_UseBackground;
	int m_Quantization;
	InterpolationMethod m_InterpolationMethod;
};

#endif 
