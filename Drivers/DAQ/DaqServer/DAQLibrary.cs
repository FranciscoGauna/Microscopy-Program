/****************************** Module Header ******************************\
* Module Name:  DAQLibrary.cs
* Project:      CSExeCOMServer
* Copyright (c) Microsoft Corporation.
* 
* The definition of the COM class, DAQLibrary, and its ClassFactory, 
* DAQLibraryClassFactory.
* 
* (Please generate new GUIDs when you are writing your own COM server) 
* Program ID: CSExeCOMServer.DAQLibrary
* CLSID_DAQLibrary: DB9935C1-19C5-4ed2-ADD2-9A57E19F53A3
* IID_IDAQLibrary: 941D219B-7601-4375-B68A-61E23A4C8425
* DIID_IDAQLibraryEvents: 014C067E-660D-4d20-9952-CD973CE50436
* 
* Properties:
* // With both get and set accessor methods
* float FloatProperty
* 
* Methods:
* // HelloWorld returns a string "HelloWorld"
* string HelloWorld();
* // DeviceList returns a list of the DAQCom devices
* List<string> DeviceList();
* // GetProcessThreadID outputs the running process ID and thread ID
* void GetProcessThreadID(out uint processId, out uint threadId);
* 
* Events:
* // FloatPropertyChanging is fired before new value is set to the 
* // FloatProperty property. The Cancel parameter allows the client to cancel 
* // the change of FloatProperty.
* void FloatPropertyChanging(float NewValue, ref bool Cancel);
* 
* 
* THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
* EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED 
* WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
\***************************************************************************/

#region Using directives
using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;
using System.ComponentModel;
#endregion

using DAQCOMLib;


namespace CSExeCOMServer {
    #region Interfaces

    [Guid(DAQLibrary.InterfaceId), ComVisible(true)]
    public interface IDAQLibrary{
        #region Properties

        #endregion

        #region Methods
        void SetDevice(string device_id);
        bool OpenDevice();
        string[] DeviceList();
        string SupportedAnalogOutputs();
        string AnalogOutputs();
        string AnalogInputs();
        bool SetAnalogInput(int channel);
        bool SetAnalogOutput(int channel, float value);
        bool SetAnalogOutputWave(int channel, float value, float freq, string wave);
        void StartScanning(int ScanCount, int ScanRate);
        void StopScanning();
        string WriteAPort(int number, float value);
        float[] ReadAPort();

        void GetProcessThreadID(out uint processId, out uint threadId);

        #endregion
    }

    [Guid(DAQLibrary.EventsId), ComVisible(true)]
    [InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
    public interface IDAQLibraryEvents{
        #region Events

        [DispId(1)]
        void FloatPropertyChanging(float NewValue, ref bool Cancel);

        #endregion
    }

    #endregion

    [ClassInterface(ClassInterfaceType.None)]           // No ClassInterface
    [ComSourceInterfaces(typeof(IDAQLibraryEvents))]
    [Guid(DAQLibrary.ClassId), ComVisible(true)]
    public class DAQLibrary : ReferenceCountedObject, IDAQLibrary {
        #region COM Component Registration

        internal const string ClassId =
            "DB9935C1-19C5-4ed2-ADD2-9A57E19F53A6";
        internal const string InterfaceId =
            "941D219B-7601-4375-B68A-61E23A4C8428";
        internal const string EventsId =
            "014C067E-660D-4d20-9952-CD973CE50439";
        
        // These routines perform the additional COM registration needed by 
        // the service.

        [EditorBrowsable(EditorBrowsableState.Never)]
        [ComRegisterFunction()]
        public static void Register(Type t){
            try {
                COMHelper.RegasmRegisterLocalServer(t);
            } catch (Exception ex) {
                Console.WriteLine(ex.Message); // Log the error
                throw ex; // Re-throw the exception
            }
        }

        internal static void Register() {
            COMHelper.RegasmRegisterLocalServer(ClassId);
        }

        [EditorBrowsable(EditorBrowsableState.Never)]
        [ComUnregisterFunction()]
        public static void Unregister(Type t){
            try {
                COMHelper.RegasmUnregisterLocalServer(t);
            } catch (Exception ex) {
                Console.WriteLine(ex.Message); // Log the error
                throw ex; // Re-throw the exception
            }
        }

        #endregion

        #region Properties

        private string device_name = "";
        private Device device;
        private int channels = 0;
        private DigitalIO digital_ios;
        private bool opened = false;
        private Acq acquire;
        private Config config;

        #endregion

        #region Methods

        public void SetDevice(string device_id) {
            device_name = device_id;
        }

        public void StartScanning(int ScanCount, int ScanRate) {
            config.ScanCount = ScanCount;
            config.ScanRate = ScanRate;
            acquire.Starts.ItemByType[StartType.sttImmediate].UseAsAcqStart();
            acquire.Stops.ItemByType[StopType.sptManual].UseAsAcqStop();
            acquire.Arm();
        }

        public void StopScanning() {
            acquire.Disarm();
            acquire.Stop();
        }

        public bool OpenDevice() {
            DaqSystem daq_system = new DaqSystem();
            acquire = daq_system.Add();
            config = acquire.Config;
            AvailableDevices available_devices = acquire.AvailableDevices;
            acquire.DataStore.AutoSizeBuffers = false;
            acquire.DataStore.BufferSizeInScans = 100000;
            acquire.DataStore.IgnoreDataStoreOverruns = true;
            if (opened) return true;

            for (int i = 1; i <= available_devices.Count; i++) {
                if (available_devices[i].Name == device_name) {
                    device = (Device)available_devices.CreateFromIndex(i);
                    device.Open();
                    device.Populate();
                    return opened = true;
                }
            }

            return false;
        }

        public string SupportedAnalogOutputs(){
            string results = "";
            for (int i = 1; i <= device.SupportedAnalogOutputs.Count; i++){
                results += device.SupportedAnalogOutputs[i].Name;
                results += ",";
                results += device.SupportedAnalogOutputs[i].ChannelCount;
                results += ",";
                results += device.SupportedAnalogOutputs[i].AnalogOutputType;
                results += ";";
			}
            return results;
        }

        public string AnalogOutputs() {
            string results = "";
            for (int i = 1; i <= device.AnalogOutputs.Count; i++){
                results += device.AnalogOutputs[i].Name;
                results += ",";
                results += device.AnalogOutputs[i].BaseChannel;
                results += ",";
                results += device.AnalogOutputs[i].AnalogOutputType;
                results += ",";
                for (int j = 1; j <= device.AnalogOutputs[i].Channels.Count; j++) {
                    results += device.AnalogOutputs[i].Channels[j].Name;
                    results += ";";
                    results += device.AnalogOutputs[i].Channels[j].Maximum;
                    results += ";";
                    results += device.AnalogOutputs[i].Channels[j].OutputChannelMode;
                }
                results += "\n";
            }
            return results;
        }
        public string AnalogInputs() {
            string results = "";
            for (int i = 1; i <= device.AnalogInputs.Count; i++) {
                results += device.AnalogInputs[i].Name;
                results += ",";
                results += device.AnalogInputs[i].BaseChannel;
                results += ",";
                results += device.AnalogInputs[i].AnalogInputType;
                results += ",";
                for (int j = 1; j <= device.AnalogInputs[i].Channels.Count; j++) {
                    results += device.AnalogInputs[i].Channels[j].Name;
                    results += ";";
                    results += device.AnalogInputs[i].Channels[j].Ranges;
                    results += ";";
                    results += device.AnalogInputs[i].Channels[j].SamplingInterval;
                }
                results += "\n";
            }
            return results;
        }

        public bool SetAnalogInput(int channel) {
            IAnalogInput pAnalogInput = null;
            for (int i = 1; i <= device.AnalogInputs.Count; i++) {
                if (device.AnalogInputs[i].BaseChannel == (DeviceBaseChannel)channel)
                    pAnalogInput = device.AnalogInputs[i];
            }
            if (pAnalogInput == null)
                return false;
            Daq3000DirectAIChannel pDirect = (Daq3000DirectAIChannel)pAnalogInput.Channels[1];
            pDirect.DifferentialMode = false;
            var pRange = pDirect.Ranges[1];
            pDirect.SelectedRange = pRange;
            pDirect.AddToScanList();

            channels += 1;
            return true; 
        }

        public bool SetAnalogOutput(int channel, float value) {
            IAnalogOutput pAnalogOutput = null;
            for (int i = 1; i <= device.AnalogOutputs.Count; i++) {
                if (device.AnalogOutputs[i].BaseChannel == (DeviceBaseChannel)channel)
                    pAnalogOutput = device.AnalogOutputs[i];
            }
            if (pAnalogOutput == null)
                return false;
            pAnalogOutput.Channels[1].OutputValue = value;
            pAnalogOutput.Channels[1].Update();
            return true;
        }

        public bool SetAnalogOutputWave(int channel, float value, float freq, string wave) {
            device.AnalogOutputs.OutputMode = WaveformOutputMode.womPredefined;
            IAnalogOutput pAnalogOutput = null;
            for (int i = 1; i <= device.AnalogOutputs.Count; i++) {
                if (device.AnalogOutputs[i].BaseChannel == (DeviceBaseChannel)channel)
                    pAnalogOutput = device.AnalogOutputs[i];
            }
            if (pAnalogOutput == null)
                return false;
            pAnalogOutput.Channels[1].OutputChannelMode = AnalogOutputChannelMode.aomWaveform;
            pAnalogOutput.Channels[1].OutputValue = value;
            pAnalogOutput.Channels[1].PredefWaveAmplitude = value;
            pAnalogOutput.Channels[1].PredefWaveFrequency = freq;
            if (wave == "SQR") {
                pAnalogOutput.Channels[1].PredefWaveType = WaveformPredefType.wptSquare;
            } else {
                pAnalogOutput.Channels[1].PredefWaveType = WaveformPredefType.wptSine;
            }
            pAnalogOutput.Channels[1].UpdateWaveform();
            return true;
        }

        public string[] DeviceList() {
            string[] devices = new string[1];
            try {
                DaqSystem daq_system = new DaqSystem();
                Acq acquire = daq_system.Add();
                AvailableDevices available_devices = acquire.AvailableDevices;
                devices = new string[available_devices.Count];
                for (int i = 1; i < available_devices.Count + 1; i++) {
                    devices[i-1] = (available_devices[i].Name);
                }
            } catch (Exception ex) {
                Console.Error.WriteLine(ex.Message);
            }
            return devices;
        }

        public string WriteAPort(int number, float value) {
            string result = device.AnalogOutputs.Count.ToString() + ", ";
            foreach(IAnalogOutput dispositivo in device.AnalogOutputs) {
                result += dispositivo.Index.ToString();
                result += ", ";
                dispositivo.Channels[1].OutputValue = value;
            }
            return result;
        }

        public float[] ReadAPort() {
            Array data = new float[channels];
            int result = acquire.DataStore.FetchData(ref data, channels);
            if (result <= 0)
                return new float[] { Single.NaN };
            return (float[])data;
        }

        public void GetProcessThreadID(out uint processId, out uint threadId) {
            processId = NativeMethod.GetCurrentProcessId();
            threadId = NativeMethod.GetCurrentThreadId();
        }

        #endregion

        #region Events

        [ComVisible(false)]
        public delegate void FloatPropertyChangingEventHandler(float NewValue, ref bool Cancel);
        public event FloatPropertyChangingEventHandler FloatPropertyChanging;

        #endregion
    }

    /// <summary>
    /// Class factory for the class DAQLibrary.
    /// </summary>
    internal class DAQLibraryClassFactory : IClassFactory {
        public int CreateInstance(IntPtr pUnkOuter, ref Guid riid, out IntPtr ppvObject) {
            ppvObject = IntPtr.Zero;

            if (pUnkOuter != IntPtr.Zero) {
                // The pUnkOuter parameter was non-NULL and the object does 
                // not support aggregation.
                Marshal.ThrowExceptionForHR(COMNative.CLASS_E_NOAGGREGATION);
            }

            if (riid == new Guid(DAQLibrary.ClassId) || riid == new Guid(COMNative.IID_IDispatch) || riid == new Guid(COMNative.IID_IUnknown)) {
                // Create the instance of the .NET object
                ppvObject = Marshal.GetComInterfaceForObject(
                    new DAQLibrary(), typeof(IDAQLibrary));
            } else {
                // The object that ppvObject points to does not support the 
                // interface identified by riid.
                Marshal.ThrowExceptionForHR(COMNative.E_NOINTERFACE);
            }

            return 0;   // S_OK
        }

        public int LockServer(bool fLock) {
            return 0;   // S_OK
        }
    }

    /// <summary>
    /// Reference counted object base.
    /// </summary>
    [ComVisible(false)]
    public class ReferenceCountedObject {
        public ReferenceCountedObject() {
            // Increment the lock count of objects in the COM server.
            ExeCOMServer.Instance.Lock();
        }

        ~ReferenceCountedObject() {
            // Decrement the lock count of objects in the COM server.
            ExeCOMServer.Instance.Unlock();
        }
    }
}
