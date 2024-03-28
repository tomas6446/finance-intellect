//| Copyright:  (C) 2015 Forex Software Ltd.                           |
//| Website:    http://forexsb.com/                                    |
//| Support:    http://forexsb.com/forum/                              |
//| License:    Proprietary under the following circumstances:         |
//|                                                                    |
//| This code is a part of Forex Strategy Builder. It is free for      |
//| use as an integral part of Forex Strategy Builder.                 |
//| One can modify it in order to improve the code or to fit it for    |
//| personal use. This code or any part of it cannot be used in        |
//| other applications without a permission.                           |
//| The contact information cannot be changed.                         |
//|                                                                    |
//| NO LIABILITY FOR CONSEQUENTIAL DAMAGES                             |
//|                                                                    |
//| In no event shall the author be liable for any damages whatsoever  |
//| (including, without limitation, incidental, direct, indirect and   |
//| consequential damages, damages for loss of business profits,       |
//| business interruption, loss of business information, or other      |
//| pecuniary loss) arising out of the use or inability to use this    |
//| product, even if advised of the possibility of such damages.       |
//+--------------------------------------------------------------------+

#property copyright "Copyright 2015, Forex Software Ltd."
#property link      "http://forexsb.com"
#property version   "2.00"

void  OnStart()
  {
   Comment("Loading...");
   int maxBars= MathMin(TerminalInfoInteger(TERMINAL_MAXBARS),100000);
   string comment="";
   ENUM_TIMEFRAMES periods[] = {PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1};
   for(int p=0;p<ArraySize(periods);p++)
     {
      comment+=ExportBars(periods[p], maxBars)+"\n";
      Comment(comment);
     }
   comment+="Ready";
   Comment(comment);
  }

string ExportBars(ENUM_TIMEFRAMES period, int maxBars)
{
   MqlRates  rates_array[];
   ArraySetAsSeries(rates_array,true);
   int bars=CopyRates(_Symbol, period, 0, maxBars, rates_array);
   string fileName = _Symbol + "_" + PeriodToStr(period) + ".csv"; // Adjusted for clarity
   string comment = "";
   if(bars > 0) // Check if there are bars to write
     {
      int filehandle = FileOpen(fileName, FILE_WRITE|FILE_CSV, ','); // Ensure comma is the separator
      if(filehandle != INVALID_HANDLE)
        {
         // Write the header
         FileWrite(filehandle, "Date", "Time", "Open", "High", "Low", "Close", "Volume");

         // Loop through the rates array and write each bar
         for(int i = bars - 1; i >= 0; i--)
           {
            FileWrite(filehandle,
                      TimeToString(rates_array[i].time, TIME_DATE), // Date
                      TimeToString(rates_array[i].time, TIME_MINUTES), // Time
                      DoubleToString(rates_array[i].open, _Digits), // Open
                      DoubleToString(rates_array[i].high, _Digits), // High
                      DoubleToString(rates_array[i].low, _Digits), // Low
                      DoubleToString(rates_array[i].close, _Digits), // Close
                      rates_array[i].tick_volume); // Volume
           }
         FileFlush(filehandle); // Make sure data is written to the file
         FileClose(filehandle); // Close the file
         comment = "File exported: " + fileName + ", " + IntegerToString(bars) + " bars";
        }
      else
        {
         comment = "Error opening file: " + fileName;
        }
     }
   else
     {
      comment = "No bars to export for: " + fileName;
     }
   return (comment);
}


string PeriodToStr(ENUM_TIMEFRAMES period)
  {
   string strper;
   switch(period)
     {
      case PERIOD_M1  : strper="1";      break;
      case PERIOD_M5  : strper="5";      break;
      case PERIOD_M15 : strper="15";     break;
      case PERIOD_M30 : strper="30";     break;
      case PERIOD_H1  : strper="60";     break;
      case PERIOD_H4  : strper="240";    break;
      case PERIOD_D1  : strper="1440";   break;
      case PERIOD_W1  : strper="10080";  break;
      case PERIOD_MN1 : strper="302400"; break;
      default : strper="";
     }
   return (strper);
  }
//+------------------------------------------------------------------+
