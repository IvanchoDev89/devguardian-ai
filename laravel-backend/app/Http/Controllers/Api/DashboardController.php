<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class DashboardController extends Controller
{
    public function stats(Request $request)
    {
        $user = $request->user();
        
        $totalScans = DB::table('scan_jobs')
            ->where('user_id', $user->id)
            ->count();
            
        $vulnerabilities = DB::table('vulnerabilities')
            ->where('user_id', $user->id)
            ->get();
            
        $critical = $vulnerabilities->where('severity', 'critical')->count();
        $high = $vulnerabilities->where('severity', 'high')->count();
        $medium = $vulnerabilities->where('severity', 'medium')->count();
        $low = $vulnerabilities->where('severity', 'low')->count();
        $fixed = $vulnerabilities->where('status', 'fixed')->count();
        
        return response()->json([
            'success' => true,
            'data' => [
                'total_scans' => $totalScans,
                'vulnerabilities' => [
                    'total' => $vulnerabilities->count(),
                    'critical' => $critical,
                    'high' => $high,
                    'medium' => $medium,
                    'low' => $low,
                    'fixed' => $fixed
                ],
                'scan_trend' => $this->getScanTrend($user->id),
                'severity_trend' => $this->getSeverityTrend($user->id)
            ]
        ]);
    }
    
    public function recentScans(Request $request)
    {
        $user = $request->user();
        
        $scans = DB::table('scan_jobs')
            ->where('user_id', $user->id)
            ->orderBy('created_at', 'desc')
            ->limit(10)
            ->get();
            
        return response()->json([
            'success' => true,
            'data' => $scans
        ]);
    }
    
    public function vulnerabilities(Request $request)
    {
        $user = $request->user();
        
        $vulnerabilities = DB::table('vulnerabilities')
            ->where('user_id', $user->id)
            ->orderBy('created_at', 'desc')
            ->limit(20)
            ->get();
            
        return response()->json([
            'success' => true,
            'data' => $vulnerabilities
        ]);
    }
    
    private function getScanTrend($userId)
    {
        $trend = [];
        for ($i = 6; $i >= 0; $i--) {
            $date = Carbon::now()->subDays($i)->format('Y-m-d');
            $count = DB::table('scan_jobs')
                ->where('user_id', $userId)
                ->whereDate('created_at', $date)
                ->count();
            $trend[] = [
                'date' => $date,
                'count' => $count
            ];
        }
        return $trend;
    }
    
    private function getSeverityTrend($userId)
    {
        return [
            'critical' => DB::table('vulnerabilities')->where('user_id', $userId)->where('severity', 'critical')->count(),
            'high' => DB::table('vulnerabilities')->where('user_id', $userId)->where('severity', 'high')->count(),
            'medium' => DB::table('vulnerabilities')->where('user_id', $userId)->where('severity', 'medium')->count(),
            'low' => DB::table('vulnerabilities')->where('user_id', $userId)->where('severity', 'low')->count()
        ];
    }
}
