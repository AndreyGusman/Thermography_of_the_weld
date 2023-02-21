

#ifndef  __USERDEF__H__  
#define  __USERDEF__H__  


#ifdef DLLPORT_EX  // define in c++ compile .
#define DLLPORT      __declspec(dllexport)
#else
#define DLLPORT      __declspec(dllimport)
#endif

typedef short INT16;
typedef signed char  INT8; 
//--------------------------------------------------------------------------------------------//
// CHANGE 2018.6  ,  COLLECT TEMP CAL TO THIS FILE ....

//max temperature iso 
#define   MAX_ISO_THERM_NUM    5 

#define   MAX_TEMP_OBJCTS_NUM   5



#define CURVE_LENGTH   16384   //49152 

#define FAULT_AD_VALUE 65535


#define CUR_INDEX_NUM     5    //���֧�ֵĵ�λ     ���ӵ�  5 �� 

//#define MAX_TEMP_OBJCTS_NUM        5//10 modified by jw 2015-06-01


// typedef unsigned char UINT8;
// typedef char INT8;
// typedef unsigned short UINT16;
// typedef short INT16;

typedef  unsigned char UINT8;
typedef  unsigned short UINT16;
typedef  unsigned int UINT32;

typedef unsigned int UINT32;
typedef int INT32;
typedef float FLOAT32;
typedef double FLOAT64;


// PALLETE TRAN OBJ 

typedef struct 
{
	char aName[4];
	char aMember1[4];
	char aMember2[4];
	unsigned short type;
	unsigned short way;
	
}unionObjPara_s; // cl  OBJECT SEND SERIAL 

typedef struct{
	char  info[1000];
}uobjInfo_s;

typedef union{

	uobjInfo_s unusedInfo;
	char  PaletteArray[256 * 4];
}paletteOrUobj_u;


typedef enum objectType_s {
	OBJECT_TYPE_NONE = 0,
	OBJECT_TYPE_RECT = 1,
	OBJECT_TYPE_SPOT = 2,
	OBJECT_TYPE_LINE = 3,
	OBJECT_TYPE_ELLIPSE = 4,
	OBJECT_TYPE_POLYGEN = 5,
} OBJECT_TYPE;


//����Ŀ�� �¶���Ϣ���ϵĵ�Ԫ�ṹ��  ��ΪCHAR *ָ������ 


typedef struct tagPointMe {
    INT16 x;
    INT16 y;
} POINTME, *PPOINTME;

typedef struct tagRectMe {
    INT16 left;
    INT16 top;
    INT16 right;
    INT16 bottom;
} RECTME, *PRECTME;

typedef struct OBJ_INFO {
    char name[4];
    union
    {
        RECTME m_rect;//
        POINTME m_point;
        //LINE line;
    };
    short emiss;
    short alarm_max_temp_10; // *10         �����õ�
    short alarm_min_temp_10; // *10 
    short type;
} obj_info_;      // FOR CL MACHINE TEMP 



#define  VERSION_MAIN       1
#define  VERSION_LOW_NEW    6  // 2017-4-22
// VERSION LOW  5 , IS BEFORE 2017-4-22

//#pragma pack(push, 1)

typedef	struct tagTRAWFileHeader 
{
	WORD		Version; 			//�汾�� FROM GUIDE IR
	WORD		VersionLow;			

	DWORD		LanguageID;			//����

	DWORD		IRBlockOffset; 		//����ͼ�����ݿ�ƫ�Ƶ�ַ 1 WORD PARALEN  ,.... PARA ..... IMG .....
	DWORD		IRBlockLength; 		//����ͼ�����ݿ鳤��

	DWORD		VLBlockOffset; 		//�ɼ���ͼ�����ݿ�ƫ�Ƶ�ַ
	DWORD		VLBlockLength; 		//�ɼ���ͼ�����ݿ鳤��

	DWORD		AudioBlockOffset; 	//�������ݿ�ƫ�Ƶ�ַ
	DWORD		AudioBlockLength; 	//�������ݿ鳤��

	DWORD		AnalysisBlockOffset; 	//�������ݿ�ƫ�Ƶ�ַ
	DWORD		AnalysisBlockLength; 	//�������ݿ鳤��

	DWORD		TextBlockOffset;		//�ı�ע�Ϳ�ƫ�Ƶ�ַ
	DWORD		TextBlockLenght;		//�ı�ע�Ϳ鳤��

	DWORD		ReservedLength;			//�����ֽڴ�С
	DWORD		Reserved[3];

}	TRAWFILEHEADER,*LPTRAWFILEHEADER;



typedef	struct tagVLParameterBlock
{
	WORD	ImageWidth;	 	//ͼ����
	WORD	ImageHeight; 	//ͼ��߶�
	WORD	dwFormat;
}  VLParameterBlock,*LPVLParameterBlock;

typedef	struct tagAudioBlock
{
	WORD	dwStereo;
	WORD	SampleRate;	 	//������
	WORD	SampleBit;	 	//��������
	DWORD	Length; 		//��������
}  AudioBlock,*LPAudioBlock;


//2010-7-20

typedef struct tagVLVideoPara{ 
	BYTE byBrighness;	
	BYTE byContrast;	
	BYTE byHue; 
	BYTE bySaturation;	
	BYTE byDefBrighness;	
	BYTE byDefContrast;	
	BYTE byDefHue; 
	BYTE byDefSaturation;	
}VLVideoPara;		//�ɼ�����Ƶ����


// ���� �ṹ �� û�е��ֽڶ���� 

typedef struct tagTVideoScopeHeader
{	//TOTAL:64bytes
	char	sType[10];			//10 
	char	sStartTime[20];		//20
	char	sEndTime[20];		//20
	char    nomean[2];
	DWORD	totalFrame;//֡��	//4
	DWORD	dwTimes;//¼��ʱ��	//4
	short   imgwid;
	short   imghei; //   ���ݵĿ� �� 
}	TVIDEOSCOPEHEAD,*LPTVIDEOSCOPEHEAD;

//#pragma pack(pop)






//#pragma pack(push, 4)
//----------------------------obj-------------------------
typedef enum OBJECT_STATE_S {
	OBJ_STATE_DEACTIVE = 0,
	OBJ_STATE_LEFT,
	OBJ_STATE_RIGHT,
	OBJ_STATE_TOP,
	OBJ_STATE_TOP_LEFT,
	OBJ_STATE_TOP_RIGHT,
	OBJ_STATE_BOTTOM,
	OBJ_STATE_BOTTON_LEFT,
	OBJ_STATE_BOTTOM_RIGHT,
	OBJ_STATE_MOVE,
	OBJ_STATE_ACTIVE
} OBJECT_STATE;

typedef struct DevRefArea_t {
	short bUseRefArea;
	short RefAreaUpX;
	short RefAreaUpY;
	short RefAreaDownX;
	short RefAreaDownY;
	short RefAreaTemp;
	short RefAreaAD;
} DevRefArea;


// ���� ������ ���¶�����Ϣ �� 
typedef struct rect_obj {

	INT16 mMaxAD; //���AD
	INT16 mMinAD; //��СAD
	INT16 mAvgAD; //ƽ��AD

	POINTME mPtMax; //��������
	POINTME mPtMin;
	union
	{
		RECTME m_rect;
		POINTME m_point;
	};
	OBJECT_TYPE ID;
	char  mDesp[4]; // old is 5 
	FLOAT32 mAvgTemp;
	FLOAT32 mMaxTemp;
	FLOAT32 mMinTemp;
	INT16 emiss;
//	INT16 m_nCurSelect;
// 	FLOAT32 alarm_max;
// 	FLOAT32 alarm_min;
// 
// 	char check_alarm_T_cnt;
// 	char check_alarm_L_cnt;
// 	int  alarm_time;
// 	int  remove_time;
} RECT_OBJ, *PRECT_OBJ,OBJ_ALL_INFO;

typedef struct _OBJ_INFO_ {

	INT8 mAlarmType; //��������
	POINTME mPtMax; //��������
	POINTME mPtMin;
	FLOAT32 mAlarmTemp; //�����¶�
	RECTME m_rect;
	char mDesp[4];

} obj_info;

//��Ư�ɼ���������
typedef struct tagSamplePara {
	int start_time; //��ʼʱ��
	int total_time; //�����ܵ�ʱ��СʱΪ��λ
	int interval_time; //�ɼ�ʱ����  ��Ϊ��λ
	int sample_num; //�����������  ʵʱ��ȥ��¼
	int end_time; //����ʱ��
	int tmp; //�ɼ��ĺ����¶�
} SAMPLE;

//�洢��Ư��Ϲ�ʽ����ϵ��
typedef struct tagGradePara {

	float K_F; //K_F
	//	unsigned short K_F;   
	short shutterTemp ; // ���ɺ�������ʱ�� ���ŵ� ��׼�¶ȣ�
	float FixedShutterTemp;   // ̽�����¶ȣ����ߵ�ѹ 
	short AddAD;   // ��Ч����������  

	// ������Ʊ 
	short  n; //3����ϵ��

	// ������ϲ���
	float Hexp0; //������
	float Hexp1; //������
	float Hexp2; //������
	short  limitL; 
	short  limitH; 
	float HexpT0; //������
	float HexpT1; //������
	float HexpT2; //������
	short  limitTL;
	short  limitTH; 
	short  resv[4]; //������

}GradePara  ;

//��Ư������
typedef struct tagTempMove {
	int shuttet_temp; //�����¶�
	int Ambient_temp; //���������¶�
	int vtemp; //1978��ѹ
	int board_temp; //��·����¶�
	short AD; //ADֵ
	short SUB_AD; //AD��ֵ
	short is_use; //��ǰֵ�Ƿ��������������
} TEMP_MOVE;




typedef struct FIT_INFO {
    
    union
    {
        double K_F;//
        double exp0;
    };
    union
    {
        double shutterTemp;//
        double exp1;
    };
    union
    {
		double fixShutterTemp;//  FST ���� 
        double exp2;
    };
    double exp3;
    double exp4;
    
    double exp5;
    double exp6;
    double exp7;
    double exp8;
    
    int gear;//��λ
    int n;//��ϴ���
} Fit_Info;


typedef enum {
	MEASURE_TYPE_SHUTTER = 0, MEASURE_TYPE_BOLD,
} MEASURETYPE;

typedef enum {
	TEMP_UNIT_CELSIUS = 0, TEMP_UNIT_FAHRENHEIT
} TEMP_UNIT;

typedef enum {
	END_TYPE_SMALL = 1, END_TYPE_BIG
} ENDTYPE;

//--------------



#define DEFAULT_EMISS                   100
#define DEFAULT_HUM                     45
#define DEFAULT_DISTANCE             	18
#define DEFAULT_K_PARAM               	78.338  //2014.8
#define DEFAULT_AD_SCALE        		1.0
#define DEFAULT_SHUTTER_TEMP    		200  // ���Ľ���
#define DEFAULT_AMBIENT_TEMP    		200
#define DEFAULT_SHUTTER_START_TEMP  	200
#define DEFAULT_CUR_LENGTH              16384//16384  change 2014.8

#define DEFAULT_BLACK_AREA_WID_HEI      20           
#define DEFAULT_BLACK_AREA_CT_X0        80   
#define DEFAULT_BLACK_AREA_CT_Y0        60


#define DEFAULT_PerCentTop_CUT          5
#define DEFAULT_PerCentDown_CUT          5

#define MEASURE_MIN_TEMP        		-2740//-400
#define MEASURE_MAX_TEMP        		10000//5000








typedef struct tagParameterLineHarware {
	unsigned short Version;    // 1
	unsigned short VersionLow; // 6 
	unsigned short ImageWidth;
	unsigned short ImageHeight;
	//unsigned short ParaHeight; // �����и߶�  �������ֻ�и�ֵ��ʹ�ã�û�б����á� Ϊ�����FPS�����������
	unsigned char ParaHeight; 
	unsigned char Cam_FPS; //CHANGE 2018.1 

	char DetectorID[8];
	char DeviceType[8];   

	unsigned short CurveIndex; //�¶ȵ�λ   �¶�����  ɫ��  1,2,3 ...

	unsigned int   ST_seconds_50X; // ����ʱ��  FRAME cnt
	short Ambient;        //̽�����¶ȣ�Ҳָ�����¶�   // ADDRESS  30.31
	short AtmosphereTemp; //�����¶�

	short VTemp;    //̽�����ܽŵ�ѹ
	short vtemp_fpa ;// ̽�����ǳ������� AD   ��PWM ռ�ձ�32767.0
	
	short KJ_Ambient;  // ���������¶� 

	// CHANGE 2018.5.15  ���ϲ���Ϊ��λ�����ݵĹؼ���Ϣ��  Ϊ�˿���
//	char  Reserved1[16];
//	char  Reserved2[16];
//	char  Reserved3[16];

	//FROM  add 2019.4 
	unsigned int det_int_val;  // 4 +  2 + 1 + 2 = 9   ,PC 48 CHAR
	unsigned short Int_Freq_div; //correction_tempture;
	unsigned char correction_gain;
	//unsigned char reserved[9];
	short    correction_b_ave; //add yzw 2018.10

	unsigned char  frame_type; //0 

	unsigned char  is_win_mode ; //add 2019.4
	unsigned short win_wid;
	unsigned short win_hei; 
	unsigned short win_stx; 
	unsigned short win_sty; 
	
	short  last_correct_vtemp ; //add 2019.5 for lwir
	
    unsigned int real_det_int_val; 
	
    //change 2020.1  for shanghai
	//char  Reserved3[16] ;  //  --88 


}PARAMETERLINEHEAD; //120   BYTE 

typedef struct tagParameterLine {
	unsigned short Version;
	unsigned short VersionLow;
	unsigned short ImageWidth;
	unsigned short ImageHeight;
	//unsigned short ParaHeight; // �����и߶�  �������ֻ�и�ֵ��ʹ�ã�û�б����á� Ϊ�����FPS�����������
	unsigned char ParaHeight; 
	unsigned char Cam_FPS; //CHANGE 2018.1 

	char DetectorID[8];
	char DeviceType[8];   

	unsigned short CurveIndex; //�¶ȵ�λ   �¶�����  ɫ��  1,2,3 ...

	unsigned int   ST_seconds_50X; // ����ʱ��  FRAME cnt
	short Ambient;        //̽�����¶ȣ�Ҳָ�����¶�   // ADDRESS  30.31
	short AtmosphereTemp; //�����¶�

	short VTemp;    //̽�����ܽŵ�ѹ
	short vtemp_fpa ;// ̽�����ǳ������� AD   ��PWM ռ�ձ�32767.0
	
	short KJ_Ambient;  // ���������¶� 

	// CHANGE 2018.5.15  ���ϲ���Ϊ��λ�����ݵĹؼ���Ϣ��  Ϊ�˿���
//	char  Reserved1[16];
//	char  Reserved2[16];
//	char  Reserved3[16];

	//FROM  add 2019.4 
	unsigned int det_int_val;  // 4 +  2 + 1 + 2 = 9   ,PC 48 CHAR
	unsigned short Int_Freq_div; //correction_tempture;
	unsigned char correction_gain;
	//unsigned char reserved[9];
	short    correction_b_ave; //add yzw 2018.10

	unsigned char  frame_type; //0 

	unsigned char  is_win_mode ; //add 2019.4
	unsigned short win_wid;
	unsigned short win_hei; 
	unsigned short win_stx; 
	unsigned short win_sty; 
	
	short  last_correct_vtemp ; //add 2019.5 for lwir
	
    unsigned int real_det_int_val; 

    //change 2020.1  for shanghai
	char  Reserved3[16] ;  // 88    2020 TO 16 

	unsigned char  M_C;
	unsigned char  M_B;
	short  L_BC_MIN  ;  // OLD IS 24 , SUB   -8  = 16
	short  L_BC_MAX  ;
	short  L_BC_MIN_CUT ;
	short  L_BC_MAX_CUT ;

	// ʵʱ����  �����￪ʼ���ǲ��°汾�ģ����� ���ÿ����ˡ� 

	//add 2018.5 ȫ�ֶ����ȶԱȶȣ�
	short    iPole;   // add 2020.1
	short    iCurrBCType;  //2018 ���ӵ�����  0  �Զ����ȶԱȶ� �� 1  �ֶ����ȶԱȶ�  ����汾�û��� 2  ȫ�û����ȶԱȶ� ����2018.5 ADD ��

	float Contrast;  // temp calc for reg
	float Brightness;
	float K_THR ; 
	short cDicardADPerCentTop;     // Լ��Ϊ ǧ�ֱ� ��
	short cDicardADPerCentBottom;  // Լ��Ϊ ǧ�ֱ� ��    -------120 

	
	UINT		m_filterType;  //��ǰʹ�õ��˲��㷨  NO .. ADD TEMP USED.   0X7777
	// �û����ݣ�  PC �û���Ҫ��ע�ģ� ����
	unsigned short PaletteIndex;


#ifdef  IS_SIGNED_OR_UNSIGNED_DATA
	short iAutoMaxAdValue;   // ʵʱ����  hist
	short iAutoMinAdValue;
	short nMaxAdValue;
	short nMinAdValue;
	short nCenterAdValue ; //���ĵ� AD  ADD YZW 
#else 
	unsigned short iAutoMaxAdValue;  // ʵʱ����  hist
	unsigned short iAutoMinAdValue;
	unsigned short nMaxAdValue;
	unsigned short nMinAdValue;
	unsigned short nCenterAdValue ; //���ĵ� AD  ADD YZW  ��Ҫ ��
	
#endif 

	short maxp_x;  // TEMP USED
	short maxp_y;
	short minp_x;
	short minp_y;
	
	float maxTemp;
	float minTemp;

	float ADScaleX;  // 1.0

	char memo[16];
	char Date[20];

	char GbitNetIpSet[32];  // "192.168.1.124"
	char VL_File_Name[16];
	char Wave_File_Name[16];

	GradePara formula[CUR_INDEX_NUM];  //OLD 96 NEW 56
	char BUFF_REV[40];  //!!!!!

	short CurveLength;   // OLD VER IS 16384 OR 8192 ....


	// �����¶����� ���ߺ����������� 
	short mAmbientIndex;
	TEMP_UNIT m_nTempUnit; 

	short TempUnit; //���µ�λ����,TEC�и���Ϊm_tecPolicy
	MEASURETYPE	mMeasureType ;  

	//unsigned short K_F;//���ߵ�б��
	float K_F;//���ߵ�б��
	short Correction_X0; 
	short Correction_X1;
	short KM_Adjust_ADD;

	unsigned short Emiss;
	unsigned short RelHum;
	unsigned short Distance;

	float mCoEfficient;   // 0 

	// Ŀǰ֧�ֵ�  5 �����Σ� 5 �� ��Ŀ��   2019 ��Ϊ 3 ����  ȫ��һ��������һ����  �û�һ����
	short obj_cnt;  //  0
	RECT_OBJ obj_info[MAX_TEMP_OBJCTS_NUM];

	// PC ������Ҫ������ 
//	short spot_cnt;
//	spot_info_ spot_info[MAX_TEMP_OBJCTS_NUM];

	short bUseRefArea;
	short RefAreaUpX;
	short RefAreaUpY;
	short RefAreaDownX;
	short RefAreaDownY;
	short RefAreaTemp;
	short RefAreaAD;

	short bUseTempPallete;   // 
	char  iISOthermNum;      //  �����¶� ɫ�� 
	char  iISOColorNum;      //
	short TempPalleteUpLimit;  // WHEN T ,  TO  nMaxAdValue ..
	short TempPalleteDownLimit;
	short ISOUP[MAX_ISO_THERM_NUM]; //AD
	short ISODOWN[MAX_ISO_THERM_NUM];
	COLORREF  ISOCOLOR[MAX_ISO_THERM_NUM]; //ADD 2020  20BIT ... ������ɫ 
	short ISOUPT[MAX_ISO_THERM_NUM]; 
	short ISODOWNT[MAX_ISO_THERM_NUM]; //TEMP
	short  mapPts[17] ; //for vl to ir 
	short  bUseMinMax ; //
	short  bUseMask; // alarm mask
	short  bUseRegionGrow; //region arith
	short  RegionIncrease; 
	short  Regionsize; 
	short  Regiondis; 
 
	char Reserved[64]; // 128 DEL ISOCOR mappts. 


	//char  PaletteArray[256 * 4];
#if 1 //cl  change 
	paletteOrUobj_u paletteOrUobj;
#endif
	// ȥ���˽ṹ�� ���ǲ������������¿��Ųɼ� ͼ��֡�����ȥ
	//TEMP_MOVE temp_move[TEMP_MOVE_NUM];

	short CurveData[CURVE_LENGTH]; // 16384  

	// WINDOWS �汾���еı���  NIOS û�� 
//#ifdef   WIN32   // FOR PC 

	char  smooth_frame_num;  //add 2015.10  ��Ӷ�֡ƽ������ Ĭ��ֵ 0 �� 

	unsigned char  SeriealPort ; // ADD 2018.5 Ϊ�� CAMLINK ���׵�SERAL ��ӵ� ���ڶ˿ں� �� 
	int   SP_band ;
	char  SP_parity ;
	int   SP_databits ; 
	int   SP_stopsbits ; 

	unsigned char   cl_cardid; 
	unsigned char   cl_chanid; 
	//char  GbitNetIpSet[32];


	char   IS_USE_M_CARD ; //for gnet for mul; 

//#endif 
	

} PARAMETERLINES, *LPPARAMETERLINES;





//----------------------------------------------------------------


#define    GETB1B2_AVERAGE_FRAME_CNT        1 // 16 

enum VIDEO_TEMP_MEASURE_STATUS
{
	GEN_Y16,
	GEN_X16,
	GET_B1,
	GET_B2_K
};


//--------------------------------------------------------------------
// old gbit use plearo  card ... 

#define	MAX_STRING_LEN			256

typedef struct  _GNET_DEVLIST_
{
	char DevName[255];
	char DevIP[255];
	char DevMAC[255];
	char DevINFO[255];
	BOOL DevEnable;
	// mcard use
    char netmask[255];
    char gateway[255];
    char dns1[255];
    char dns2[255];
	
}GNET_DEVLIST, MNET_DEVLIST;

//��Ϣ�ṹ
#define WM_NETCARD_GETCMD		(WM_USER + 0x5050)
typedef struct _tagGNET_CMD_
{
    unsigned char lData[MAX_STRING_LEN];
	unsigned int lSize; 
}GNET_COMMAND;

typedef int (WINAPI* MessageFilter)(void *pUserData, unsigned short messageID, unsigned char *pData, unsigned int length);



extern "C" { 
//�豸����     
//����IP��ַ���豸  ���ھ������������Ϣ
int  DLLPORT GBitnetSearch(GNET_DEVLIST *m_Gnet_card_list);   //���������������
int  DLLPORT IR_GnetOpen(HWND hwnd, char *IPAddr,int bGrab=0,int packetsize=1440, int skip=0);


//	���������	
//	hwnd��		��Ϣ�����ھ��
//	IPAddr��	����IP��ַ    ��ʽΪ[192.168.1.22]
//	bGrab       ���ݽ��տ��Բ����������պ��û�������׽ģʽ���ص�����ֻ����bGrab=0 ����������ģʽ��ʹ��
//  packetsize  ͼ�����ݴ���ʱ��ÿ�����Ĵ�С  ������ 32 �ı��� 
//	skip        �����ɼ�ģʽ�²ɼ��ļ��
//	����ֵ��
//	> 0 ���ӵ�������Ĳ������
//	<= 0 ����ʧ��
BOOL DLLPORT IR_SetGnetStreamCapInterval(int handle, int skipcnt);   // ��������ǧ����ͨ�� 
int  DLLPORT IR_GetGnetStreamCapInterval(int handle);  


};

//-------------------------------------------------------------------------------------


const short MAX_SIGCHARBUFFER	=	255;

//added by jw 2017-05-17
#define DEVICE_MODEL       ("G003L")
#define DETECTOR_TYPE	    ("MT6415")
#define DETECTOR_SERIAL_NUM		("00000001")

//added by jw 2017-04-09
//configuration register
#define	AVALON_DET_DEFAULT_CONFIG_VALUE			(0x8ba00087)
//integration time register
#define	AVALON_DET_DEFAULT_INT_TIME_VALUE			(1000)
#define	AVALON_DET_DEFAULT_INT_TIME_MIN			(1)
#define	AVALON_DET_DEFAULT_INT_TIME_MAX			(217310)

#define AVALON_DET_CONFIG_VALUE         (AVALON_DET_DEFAULT_CONFIG_VALUE)
#define AVALON_DET_INT_TIME_VALUE       (AVALON_DET_DEFAULT_INT_TIME_VALUE)
#define AVALON_DET_INT_TIME_MIN         (AVALON_DET_DEFAULT_INT_TIME_MIN)
#define AVALON_DET_INT_TIME_MAX         (AVALON_DET_DEFAULT_INT_TIME_MAX)




//VSK��ѹĿ��ֵ5.12V����ֵ3900����·�Ŵ�ϵ��Ϊ1.243
//GFID��ѹĿ��ֵ3.00V����ֵ2900����·�޷Ŵ�
#define I2C_AD5339_VDETCOM_DIGIT	(2250)//(3900)
#define I2C_AD5339_VREF_DIGIT		(2700)//(2900)
#define I2C_AD5339_VSK_DIGIT		(I2C_AD5339_VDETCOM_DIGIT)
#define I2C_AD5339_GFID_DIGIT		(I2C_AD5339_VREF_DIGIT)
//VBUS��ѹĿ��ֵ2.80V,��Ӧ��ֵ2680��Ŀǰ��·������2.771V
//GSK��ѹĿ��ֵ2.12V����Ӧ��ֵ2050��Ŀǰ��·������2.109V
#define	I2C_AD5339_VBUS_DIGIT		(2680)
#define	I2C_AD5339_GSK_DIGIT		(2050)

#define	BIAS_VSK_DIGIT				(I2C_AD5339_VSK_DIGIT)
#define	BIAS_GFID_DIGIT				(I2C_AD5339_GFID_DIGIT)
#define	BIAS_VBUS_DIGIT				(I2C_AD5339_VBUS_DIGIT)
#define	BIAS_GSK_DIGIT				(I2C_AD5339_GSK_DIGIT)


// 262144  one block
// 64 BLOCK
#define FLASH_MEM_SIZE              (16777216)  //falsh size 16MB=16777216Byte
#define STORAGEBLOCK_NUM            (36)        //16M һ����  64 ���� �� ʹ���� 36���� 3+3 + 30


//added by jw 2017-04-09
typedef struct _CONFIG_ARG_ {
	//�Ƿ��ǵ�һ������
	short FIRST_CONFIG ;

	//-------------���ܲ���-----------------------

	//�������Ҫ��ʱ��֡��Ĭ��Ϊ5֡ ���Ŵ���ȥ
	short SEND_SHUTTER_CNT;
	//���Ż���
	short SEND_SHUTTER_BACK_CNT;

	//����У����Ҫ�����֡��Ĭ��Ϊ8֡
	short CWWAITKM_CNT;

	//��о�ȶ�����೤ʱ���һ�ο���Ĭ��Ϊ300�� 
	short SENDSHUTTER_TIME;     //

	//�Զ������ 
	short SENDSHUTTER_AUTO_MODE;  // -1  ������һ�Σ� 0  ʼ�ղ���  1  �Զ��� ���� SENDSHUTTER_TIME ���ġ�

	// 2019.12 for sync mode
	short SYNC_MODE;  // SYS_REV0;

	//���ȶԱȶ�֡ƽ��������Ĭ��Ϊ8
	short SMOOTH_FRAME_CNT;

	//�ֶ����ڶԱȶȵĲ���Ĭ��24
//	short BLACKBODY_WID;
	short NOUSED0;
	//�ֶ��������Ȳ���Ĭ�� 12
	short NOUSED1;


	//�����ײ��׵�����
	short NOUSED3; //  HIST_CUT_CNT;
	//�Զ����ȶԱȶ�״̬�µĶԱȶ�����ֵĬ��Ϊ2048
	short NOUSED4 ; //  AUTO_CON_LIMIT_UP;
	//�ֶ�״̬�¶Աȶ�����
	//short MANUAL_CON_LIMIT_UP;  // CHANGE 2018.10
	short   Image_ave; //

	//---------------------------1979����------------
	// 2016.3 �Ķ��� ȥ��ԭ��  TEMP_1979_LOW_LIMIT TEMP_1979_HIGH_LIMIT 
	short START_1979_UP_VALUE;    // �����¶� �����ϴο����¶ȣ���������ʹ�á�  
	//short Int_Resv0;   //����ʱ��Ԥ��  

	// �������Ӧ��    ��λ�ò��䣬����ԭ�������ݽṹ�� 
	// �Զ�����ʱ�� �� ��ز�������������

	short AutoInt_POLICY;      // �Ƿ�����Զ�����  0 �������ã� 1 ���� 
	// // �Զ��ع� Ŀ��AD ƽ��� ��
	short AutoIntDestAd;         



	//1979�����¶ȵ�
	short WORK_1979_TEMP;

	//�¿ز���
	short CT_POLICY ;

	// ADD YZW ƫѹ���� 
	unsigned short VSK;  // һ��Ϊ 
	unsigned short GFID; // һ��Ϊ 
	unsigned short VBUS; //2.8   25mv
	unsigned short GSK;  //2.12  50mv

	// ADD 2016.3  PID 
	unsigned  short Kp; 
	unsigned  short Ki; 
	unsigned  short Kd; 

	//modified by jw 2018-05-25
	//adc clok phase shift object:unit is ps.
	 int phase_object;//SYS_REV1 ;  // change to int  unsigned .  

	short FlashValidPage;

	//����Ϊ  ̽�������� ��
	 //����ʱ�䱶����ʵ����֡Ƶ��Ƶ����n=1,2,4,8...,2^N.��
	unsigned short  Int_Freq_div;

	//	unsigned int SENSOR_SERIAL_DATA;
	//̽��������ʱ�������΢�����̽��������ʱ��������
	//���ݲ�ͬ̽����ȷ����Ŀǰ��󲻳���24λ
	unsigned int Int_time;

	//��ͬ����̽�����Ĵ����������ݣ�λ�������ݣ���ͬ
	//�������32λʱ���ݾ����������±����32λ
	// ����-��ת-�ڲ�ƫѹ-ͨ��
	//  2   - 3 - 12  -- 3 ,
	unsigned int SENSOR_SERIAL_DATA0;  //

	//modified by jw 2017-05-17
	//min integral time
	unsigned int SENSOR_SERIAL_DATA1;
	//max integral time
	unsigned int SENSOR_SERIAL_DATA2;
	//detector type name,such as "ISC0002"
	char detector_type[16];
	//detector serial num, such as "12345678"
	char detector_serial_num[16];
	//device model name,such as "G003L"
	char device_model[16];
	//device communication interface type name,such as "IRUSBFT"
	char device_comm_if_type0[16];
	char device_comm_if_type1[16];
	
	//
	unsigned short hardware_version;
	unsigned short software_version;
	//the time of latest software revision
	//[31:20]~year,[19:16]~month,[15:11]~day,
	//[10:6]~hour,[5:0]~minute
	unsigned int hardware_revision_time;
	//the time of latest software revision
	//[31:20]~year,[19:16]~month,[15:11]~day,
	//[10:6]~hour,[5:0]~minute
	unsigned int software_revision_time;

//	unsigned int det_int_val[10];
	//ADD YZW 2018.7
	int     resv_2018 ;  //V1V2 �汾Ϊ    phase_object BUT  NEW 2018.10 CORE USE UP..
	// ARITH or para ;  add 2018.12 
	short   col_arith_type;
	short   col_add[8];

	unsigned short FRAME_SKIP_CNT;


} CONFIG , *pCONFIG;

//#pragma pack(pop)

//-------------------------------------------------------------------------


//-------------------------------------------------------------------------

extern "C"
{
	//һ�����ڲ�����ʹ�õġ� 
	
	int DLLPORT  IR_GetLostFrameCnt(void * handle); // for test 
    BOOL DLLPORT IR_EnableSaveBP(void * handle, int mode);
	
	// �ڲ�ʹ��  
    BOOL DLLPORT  IR_DebugSet(void * handle,BOOL set);	        
	void DLLPORT  IR_DebugGetPara(void * handle,short xishu[10]);  
	BOOL DLLPORT  IR_DebugSetPara(void * handle,short xishu[10]);  
	// �㷨ʹ��  
	BOOL DLLPORT  IR_SetArithType(void * handle, int type);  
	int  DLLPORT  IR_GetCurrArithType(void * handle);  
	
	
	// 2014 ���ӻ���ӿ� 
    short   DLLPORT  * IR_GetDevieceBpImage(void * handle);
    void    DLLPORT   IR_SetDevieceBpImage(void * handle,short * image);  //SDK����Ļ�����Ϣ�� 
	
	
	//  ��λ������ʱ������⣬ 
	
	
	//   int   DLLPORT IR_SetSysConfigPara(int handle,void * para); 
	
	void  DLLPORT time_init(void);
	
	int   DLLPORT get_time_begin(void);
	int   DLLPORT get_time_end(void);
	int   DLLPORT get_time_span(void);
	void  DLLPORT time_delay(int milli_seconds);

};






#endif 
