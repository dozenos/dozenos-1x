<!-- included start from vni-tagnode.xml.i -->
<tagNode name="vni">
  <properties>
    <help>VXLAN network identifier (VNI) number</help>
    <completionHelp>
      <list>&lt;1-16777215&gt;</list>
      <script>${dozenos_completion_dir}/list_vni.sh</script>
    </completionHelp>
  </properties>
  <command>${dozenos_op_scripts_dir}/evpn.py show_evpn --command "$*"</command>
</tagNode>
<!-- included end -->
